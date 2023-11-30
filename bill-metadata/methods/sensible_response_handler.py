import json
from calendar import monthrange
from datetime import datetime


class SensibleResponseHandler:
    def __init__(self, json_response: dict, carrier: str, bigquery_uuid: str):
        """
        Initialize the SensibleResponseHandler.
        """
        self.full_response = json_response
        self.carrier = carrier
        self.bigquery_uuid = bigquery_uuid
        self.parsed_document = json_response["parsed_document"]

    def process_response(self):
        """
        Process the JSON data based on carrier-specific rules.
        """
        # FOR DEVELOPMENT
        with open(
            "/Users/kieranshaw/audit-bill-extraction/responses/sample.json", "w"
        ) as file:
            json.dump(self.full_response, file, indent=4)

        if self.carrier == "unitedhealthcare":
            return self._process_for_unitedhealthcare()
        else:
            parsed_object = {
                "bigquery_id": self.bigquery_uuid,
                "sensible_id": self.full_response["id"],
                "parsed_validated": {
                    "total_current_premium": self.full_response["parsed_document"][
                        "total_current_premium"
                    ]["value"],
                    "billing_start_date": self.full_response["parsed_document"][
                        "billing_start_date"
                    ]["value"],
                    "billing_end_date": self.full_response["parsed_document"][
                        "billing_end_date"
                    ]["value"],
                },
            }
            return parsed_object

    def _process_for_unitedhealthcare(self):
        """
        Process data for unitedhealthcare.
        """
        billing_start_date = self._raw_billing_period_to_start_date(
            raw_billing_period=self.full_response["parsed_document"][
                "_raw_billing_period"
            ]["value"]
        )
        billing_end_date = self._raw_billing_period_to_end_date(
            raw_billing_period=self.full_response["parsed_document"][
                "_raw_billing_period"
            ]["value"]
        )

        parsed_object = {
            "bigquery_id": self.bigquery_uuid,
            "sensible_id": self.full_response["id"],
            "parsed_validated": {
                "total_current_premium": self.full_response["parsed_document"][
                    "total_current_premium"
                ]["value"],
                "billing_start_date": billing_start_date,
                "billing_end_date": billing_end_date,
            },
        }
        return parsed_object

    def _raw_billing_period_to_start_date(self, raw_billing_period: str):
        parsed_date = datetime.strptime(raw_billing_period, "%B %Y")
        year = parsed_date.year
        month = parsed_date.month
        first_day = datetime(year, month, 1)
        start_date_formatted = first_day.strftime("%Y-%m-%dT00:00:00.000Z")
        return start_date_formatted

    def _raw_billing_period_to_end_date(self, raw_billing_period: str):
        parsed_date = datetime.strptime(raw_billing_period, "%B %Y")
        year = parsed_date.year
        month = parsed_date.month
        last_day = datetime(year, month, monthrange(year, month)[1])
        end_date_formatted = last_day.strftime("%Y-%m-%dT00:00:00.000Z")
        return end_date_formatted
