import json

class ClientDataParser:
    def __init__(self, json_text):
        """
        Initialize the parser with JSON input.

        Args:
            json_text (str): The input JSON string containing data to parse.
        """
        self.json_text = json_text
        self.parsed_data = []

    def extract_flag_data(self):
        """
        Extract FLAG:, ID, the number after ID, and text after "capped the" from JSON.
        """
        try:
            data = json.loads(self.json_text)
            for entry in data:
                if "FLAG" in entry and "ID" in entry and "TeamFlag" in entry:
                    self.parsed_data.append({
                        'ID': str(entry["ID"]),
                        'Team': entry["TeamFlag"]
                    })
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    def get_parsed_data(self):
        """
        Get the parsed data.

        Returns:
            list: List of dictionaries with parsed data.
        """
        return self.parsed_data

# Example usage
if __name__ == "__main__":
    sample_json = """
    [
        {"FLAG": true, "ID": 2049, "TeamFlag": "Diamond Sword flag"},
        {"FLAG": true, "ID": 3051, "TeamFlag": "Blood Eagle flag"}
    ]
    """

    parser = ClientDataParser(sample_json)
    parser.extract_flag_data()
    print("Parsed Data:", parser.get_parsed_data())
