import os
import kagglehub
import shutil
import zipfile

from src.logger import get_logger
from src.custom_exception import CustomException
from config.data_ingestion_config import *


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, dataset_name: str, target_dir: str):
        self.dataset_name = dataset_name
        self.target_dir = target_dir

    def create_raw_dir(self):
        raw_dir = os.path.join(self.target_dir, "raw")
        if not os.path.exists(raw_dir):
            try:
                os.makedirs(raw_dir)
                logger.info(f"Created directory: {raw_dir}")
            except Exception as e:
                logger.error("Error while creating the raw directory")
                raise CustomException("Failed to create the raw dir", e)
        return raw_dir
    
    def extract_image_labels(self, path: str, raw_dir: str):
        try:
            extract_dir = path
            if path.endswith('.zip'):
                logger.info("Extracting the zip file...")
                extract_dir = os.path.dirname(path)   # extract into parent folder
                with zipfile.ZipFile(path, 'r') as ref_zip:
                    ref_zip.extractall(extract_dir)
                logger.info(f"Extracted zip file into: {extract_dir}")

            images_folder = os.path.join(extract_dir, "Images")
            labels_folder = os.path.join(extract_dir, "Labels")

            # Move Images folder
            target_images = os.path.join(raw_dir, "Images")
            if os.path.exists(images_folder):
                if not os.path.exists(target_images):
                    shutil.move(images_folder, target_images)
                    logger.info(f"Images moved successfully to: {target_images}")
                else:
                    logger.warning("Images folder already exists in raw_dir. Skipping move.")
            else:
                logger.warning("Images folder not found after extraction.")
            
            # Move Labels folder
            target_labels = os.path.join(raw_dir, "Labels")
            if os.path.exists(labels_folder):
                if not os.path.exists(target_labels):
                    shutil.move(labels_folder, target_labels)
                    logger.info(f"Labels moved successfully to: {target_labels}")
                else:
                    logger.warning("Labels folder already exists in raw_dir. Skipping move.")
            else:
                logger.warning("Labels folder not found after extraction.")
            
        except Exception as e:
            logger.error("Error while moving directories")
            raise CustomException("Error while moving the directories", e)
        
    def downloads_dataset(self, raw_dir: str):
        try:
            path = kagglehub.dataset_download(self.dataset_name)
            logger.info(f"Downloaded dataset from: {self.dataset_name}")

            # Extract images and labels
            self.extract_image_labels(path, raw_dir)

        except Exception as e:
            logger.error("Error while downloading the dataset")
            raise CustomException("Error while downloading the dataset", e)
    
    def run(self):
        try:
            raw_dir = self.create_raw_dir()
            self.downloads_dataset(raw_dir=raw_dir)
        except Exception as e:
            logger.error("Error in data ingestion pipeline")
            raise CustomException("Error in data ingestion pipeline", e)


if __name__ == "__main__":
    data_ingestion = DataIngestion(DATASET_NAME, TARGET_DIR)
    data_ingestion.run()