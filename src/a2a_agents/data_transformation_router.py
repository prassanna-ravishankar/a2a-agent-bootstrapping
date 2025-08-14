"""FastAPI router for the Data Transformation Agent."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .data_transformation_agent import transform_data
from .models import DataTransformationRequest, DataTransformationResult, TargetFormat


# Create the router for the Data Transformation Agent
data_transformation_router = APIRouter(
    prefix="/data",
    tags=["data-transformation"],
    responses={404: {"description": "Not found"}},
)


@data_transformation_router.post("/transform", response_model=DataTransformationResult)
async def data_transform_endpoint(request: DataTransformationRequest) -> DataTransformationResult:
    """Data Transformation Agent endpoint for cleaning and structuring data.
    
    Args:
        request: Data transformation request
        
    Returns:
        Transformed data in the requested format
    """
    try:
        result = await transform_data(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data transformation failed: {str(e)}")


@data_transformation_router.get("/formats")
async def get_supported_formats():
    """Get list of supported transformation formats."""
    return JSONResponse(
        content={
            "supported_formats": [format_type.value for format_type in TargetFormat],
            "format_descriptions": {
                "json": "JavaScript Object Notation - structured data format",
                "csv": "Comma-Separated Values - tabular data format",
                "xml": "Extensible Markup Language - hierarchical data format",
                "yaml": "YAML Ain't Markup Language - human-readable data format",
                "markdown": "Markdown - formatted text with simple syntax",
                "html": "HyperText Markup Language - web document format"
            }
        }
    )


@data_transformation_router.get("/health")
async def data_health_check():
    """Health check endpoint for the Data Transformation Agent."""
    return JSONResponse(
        status_code=200,
        content={
            "agent": "Data Transformation Agent 🔄",
            "status": "healthy",
            "capabilities": [
                "Data format detection and parsing",
                "Data cleaning and normalization",
                "Multi-format transformation",
                "URL data fetching"
            ]
        }
    )


@data_transformation_router.get("/info")
async def data_info():
    """Information endpoint for the Data Transformation Agent."""
    return JSONResponse(
        content={
            "name": "Data Transformation Agent",
            "emoji": "🔄",
            "description": "Cleans and structures raw, messy data into specified formats",
            "input_format": {
                "data": "string - Raw data (text or URL)",
                "target_format": "string - Target format (json, csv, xml, yaml, markdown, html)"
            },
            "output_format": {
                "transformed_data": "string - Data transformed to the requested format"
            },
            "supported_input_formats": [
                "JSON", "CSV", "TSV", "XML", "YAML", "Unstructured Text", "URLs"
            ],
            "supported_output_formats": [format_type.value for format_type in TargetFormat],
            "example_input": {
                "data": "name,age,city\nJohn,25,New York\nJane,30,Boston",
                "target_format": "json"
            }
        }
    )


# Export the router
__all__ = ['data_transformation_router']
