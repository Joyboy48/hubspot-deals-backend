import dlt   # 👈 YE LINE ADD KARO

class ExtractionService:
    def __init__(self, config: dict):
        self.config = config
        self.pipeline = dlt.pipeline(
            pipeline_name="hubspot_deals_pipeline",
            destination="postgres",
            dataset_name="hubspot_deals"
        )


    def start_scan(self, validated_config: dict):
        access_token = validated_config["auth"]["accessToken"]

        self.pipeline.run(
            hubspot_deals_resource(access_token=access_token)
        )

        return {"status": "completed"}

    def get_pipeline_info(self):
        return {
            "pipeline_name": self.pipeline.pipeline_name,
            "destination": "postgres",
            "dataset": self.pipeline.dataset_name
        }
