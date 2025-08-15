"""Data Transformation Agent for cleaning and structuring messy data."""

import csv
import json
import re
from io import StringIO
from typing import Any, Dict, List
from urllib.parse import urlparse

import httpx
import yaml
from pydantic_ai import Agent, RunContext

from ..config import MODEL_NAME
from ..models import DataTransformationRequest, DataTransformationResult, TargetFormat


# System prompt for the data transformation agent
DATA_TRANSFORMATION_SYSTEM_PROMPT = """
You are an expert Data Transformation Agent specializing in cleaning, structuring, and converting messy data into well-organized formats.

Your capabilities:
1. Parse and understand various data formats and structures
2. Clean messy, inconsistent, or malformed data
3. Transform data into specified target formats (JSON, CSV, XML, YAML, Markdown, HTML)
4. Handle missing values, inconsistencies, and data quality issues
5. Extract structured information from unstructured text
6. Preserve data integrity while improving organization

Your tasks:
- Analyze input data to understand its structure and content
- Identify and resolve data quality issues
- Transform data into the requested target format
- Ensure output is valid and well-structured
- Maintain data relationships and context during transformation

Guidelines:
- Always validate and clean input data before transformation
- Handle edge cases gracefully (missing values, malformed entries)
- Preserve important information during conversion
- Use consistent formatting and naming conventions
- Provide clear structure in the output format
- For tabular data, maintain relationships between columns
- For hierarchical data, preserve parent-child relationships
- When transforming to markup formats, ensure proper escaping and formatting

Format-specific guidelines:
- JSON: Use proper data types, avoid redundant nesting
- CSV: Include headers, handle special characters properly
- XML: Use meaningful tag names, proper nesting structure
- YAML: Maintain readability with proper indentation
- Markdown: Use appropriate headings and formatting
- HTML: Create semantic, well-formed markup
"""


def is_url(text: str) -> bool:
    """Check if the given text is a valid URL."""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


async def fetch_data_from_url(url: str) -> str:
    """Fetch data from a URL.
    
    Args:
        url: The URL to fetch data from
        
    Returns:
        The fetched data as a string
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch data from URL: {e}")


def detect_data_format(data: str) -> str:
    """Detect the format of the input data.
    
    Args:
        data: The input data string
        
    Returns:
        Detected format as a string
    """
    # Remove leading/trailing whitespace
    data = data.strip()
    
    # Check for JSON
    if (data.startswith('{') and data.endswith('}')) or (data.startswith('[') and data.endswith(']')):
        try:
            json.loads(data)
            return "JSON"
        except json.JSONDecodeError:
            pass
    
    # Check for XML
    if data.startswith('<') and data.endswith('>'):
        return "XML"
    
    # Check for YAML
    if ':' in data and not data.startswith('<'):
        try:
            yaml.safe_load(data)
            return "YAML"
        except yaml.YAMLError:
            pass
    
    # Check for CSV (simple heuristic)
    if ',' in data and '\n' in data:
        lines = data.split('\n')
        if len(lines) > 1:
            first_line_commas = lines[0].count(',')
            second_line_commas = lines[1].count(',')
            if first_line_commas > 0 and abs(first_line_commas - second_line_commas) <= 1:
                return "CSV"
    
    # Check for TSV
    if '\t' in data and '\n' in data:
        return "TSV"
    
    return "Unstructured Text"


def clean_and_parse_data(data: str) -> Dict[str, Any]:
    """Clean and parse the input data into a structured format.
    
    Args:
        data: Raw input data
        
    Returns:
        Parsed and cleaned data structure
    """
    detected_format = detect_data_format(data)
    
    try:
        if detected_format == "JSON":
            return json.loads(data)
        
        elif detected_format == "YAML":
            return yaml.safe_load(data)
        
        elif detected_format == "CSV":
            # Parse CSV data
            reader = csv.DictReader(StringIO(data))
            return {"data": list(reader), "format": "tabular"}
        
        elif detected_format == "TSV":
            # Parse TSV data
            reader = csv.DictReader(StringIO(data), delimiter='\t')
            return {"data": list(reader), "format": "tabular"}
        
        else:
            # For unstructured text, try to extract meaningful information
            return {
                "content": data,
                "format": "text",
                "detected_format": detected_format
            }
    
    except Exception as e:
        # Fallback to treating as plain text
        return {
            "content": data,
            "format": "text",
            "error": f"Parsing error: {e}",
            "detected_format": detected_format
        }


def transform_to_json(data: Dict[str, Any]) -> str:
    """Transform data to JSON format."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def transform_to_csv(data: Dict[str, Any]) -> str:
    """Transform data to CSV format."""
    if isinstance(data, dict) and "data" in data and data.get("format") == "tabular":
        # Already tabular data
        tabular_data = data["data"]
    elif isinstance(data, list):
        tabular_data = data
    elif isinstance(data, dict):
        # Convert dict to tabular format
        if all(isinstance(v, (str, int, float, bool)) for v in data.values()):
            # Simple flat dict
            tabular_data = [data]
        else:
            # Complex dict - flatten first level
            flattened = []
            for key, value in data.items():
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        flattened.append({"key": key, "index": i, "value": str(item)})
                else:
                    flattened.append({"key": key, "value": str(value)})
            tabular_data = flattened
    else:
        tabular_data = [{"value": str(data)}]
    
    if not tabular_data:
        return "No data to convert to CSV"
    
    # Create CSV
    output = StringIO()
    fieldnames = list(tabular_data[0].keys()) if tabular_data else []
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tabular_data)
    
    return output.getvalue()


def transform_to_xml(data: Dict[str, Any]) -> str:
    """Transform data to XML format."""
    def dict_to_xml(d: Dict[str, Any], root_tag: str = "data") -> str:
        xml_parts = [f"<{root_tag}>"]
        
        for key, value in d.items():
            # Clean key for XML tag
            clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', str(key))
            
            if isinstance(value, dict):
                xml_parts.append(dict_to_xml(value, clean_key))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        xml_parts.append(dict_to_xml(item, clean_key))
                    else:
                        xml_parts.append(f"<{clean_key}>{str(item)}</{clean_key}>")
            else:
                xml_parts.append(f"<{clean_key}>{str(value)}</{clean_key}>")
        
        xml_parts.append(f"</{root_tag}>")
        return "\n".join(xml_parts)
    
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{dict_to_xml(data)}'


def transform_to_yaml(data: Dict[str, Any]) -> str:
    """Transform data to YAML format."""
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)


def transform_to_markdown(data: Dict[str, Any]) -> str:
    """Transform data to Markdown format."""
    def dict_to_markdown(d: Dict[str, Any], level: int = 1) -> str:
        md_parts = []
        
        for key, value in d.items():
            header = "#" * min(level, 6)
            md_parts.append(f"{header} {key}\n")
            
            if isinstance(value, dict):
                md_parts.append(dict_to_markdown(value, level + 1))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        md_parts.append(dict_to_markdown(item, level + 1))
                    else:
                        md_parts.append(f"- {str(item)}")
                md_parts.append("")
            else:
                md_parts.append(f"{str(value)}\n")
        
        return "\n".join(md_parts)
    
    return dict_to_markdown(data)


def transform_to_html(data: Dict[str, Any]) -> str:
    """Transform data to HTML format."""
    def dict_to_html(d: Dict[str, Any], level: int = 1) -> str:
        html_parts = []
        
        for key, value in d.items():
            header_tag = f"h{min(level, 6)}"
            html_parts.append(f"<{header_tag}>{str(key)}</{header_tag}>")
            
            if isinstance(value, dict):
                html_parts.append(dict_to_html(value, level + 1))
            elif isinstance(value, list):
                html_parts.append("<ul>")
                for item in value:
                    if isinstance(item, dict):
                        html_parts.append("<li>")
                        html_parts.append(dict_to_html(item, level + 1))
                        html_parts.append("</li>")
                    else:
                        html_parts.append(f"<li>{str(item)}</li>")
                html_parts.append("</ul>")
            else:
                html_parts.append(f"<p>{str(value)}</p>")
        
        return "\n".join(html_parts)
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Transformed Data</title>
</head>
<body>
{dict_to_html(data)}
</body>
</html>"""


# Create the data transformation agent
data_transformation_agent = Agent(
    MODEL_NAME,
    system_prompt=DATA_TRANSFORMATION_SYSTEM_PROMPT,
    deps_type=RunContext,
)


@data_transformation_agent.tool
async def analyze_and_clean_data(ctx: RunContext, raw_data: str) -> str:
    """Analyze and clean the input data.
    
    Args:
        ctx: The run context
        raw_data: Raw input data to analyze
        
    Returns:
        Analysis and cleaning recommendations
    """
    detected_format = detect_data_format(raw_data)
    parsed_data = clean_and_parse_data(raw_data)
    
    return f"""
Data Analysis Results:
- Detected format: {detected_format}
- Data structure: {type(parsed_data)}
- Sample content: {str(parsed_data)[:500]}...
"""


async def transform_data(request: DataTransformationRequest) -> DataTransformationResult:
    """Transform data to the specified format.
    
    Args:
        request: Data transformation request
        
    Returns:
        Transformed data result
    """
    raw_data = request.data
    
    # Check if data is a URL
    if is_url(raw_data):
        try:
            raw_data = await fetch_data_from_url(raw_data)
        except Exception as e:
            return DataTransformationResult(
                transformed_data=f"Error fetching data from URL: {e}"
            )
    
    # Let the AI agent analyze and suggest improvements
    result = await data_transformation_agent.run(
        f"""Please analyze and transform the following data to {request.target_format.value.upper()} format:

Raw Data:
{raw_data}

Target Format: {request.target_format.value.upper()}

Please:
1. Use the analyze_and_clean_data tool to understand the data structure
2. Clean and normalize the data as needed
3. Transform it to the target format with proper structure
4. Ensure the output is valid and well-formatted

Provide only the transformed data as your final response."""
    )
    
    # Parse and clean the data
    parsed_data = clean_and_parse_data(raw_data)
    
    # Transform to the target format
    try:
        if request.target_format == TargetFormat.JSON:
            transformed = transform_to_json(parsed_data)
        elif request.target_format == TargetFormat.CSV:
            transformed = transform_to_csv(parsed_data)
        elif request.target_format == TargetFormat.XML:
            transformed = transform_to_xml(parsed_data)
        elif request.target_format == TargetFormat.YAML:
            transformed = transform_to_yaml(parsed_data)
        elif request.target_format == TargetFormat.MARKDOWN:
            transformed = transform_to_markdown(parsed_data)
        elif request.target_format == TargetFormat.HTML:
            transformed = transform_to_html(parsed_data)
        else:
            transformed = f"Unsupported target format: {request.target_format}"
    except Exception as e:
        transformed = f"Error during transformation: {e}"
    
    # Use AI-enhanced version if available, otherwise fallback to our transformation
    ai_result = result.data if result.data else ""
    final_result = ai_result if len(ai_result) > len(transformed) else transformed
    
    return DataTransformationResult(
        transformed_data=final_result
    )


# Export the main function
__all__ = ['transform_data', 'data_transformation_agent']
