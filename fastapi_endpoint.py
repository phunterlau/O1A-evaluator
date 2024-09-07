import os
import traceback
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from workflow_driver import process_cv, generate_markdown_summary
import tempfile
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/process_cv/")
async def process_cv_endpoint(file: UploadFile = File(...)):
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Process the CV
        result = process_cv(temp_file_path)
        
        # Generate markdown summary
        summary = generate_markdown_summary(result)
        
        # Add the summary to the result
        result["markdown_summary"] = summary
        
        # Return the full output as JSON
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)