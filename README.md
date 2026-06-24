# Amazon PTO Calculator

The Amazon PTO Calculator is a Python script designed to calculate and visualize the Paid Time Off (PTO) hours for Amazon corporate staff. It retrieves PTO data from an OpenDocument Spreadsheet (`amazon_vacation_schedule.ods`) and performs calculations based on the specified parameters. 

User-specific configuration is stored in `config.toml` (you can copy `config.toml.example` to `config.toml` and modify configuration as needed.

The path to `amazon_vacation_schedule.ods` is set via the `schedule_file` key in `config.yaml`. The spreadsheet should follow the schema:

| end_date  | standard | flexible |
|-----------|----------|----------|
| 1/31/2025 |          | 8        |
| 2/28/2025 |          |          |
| 3/31/2025 | 48       |          |

Where:
- `end_date` is the month-end date
- `standard` and `flexible` are the number of hours taken during the month


## Usage

To use the Amazon PTO Calculator, follow these steps:

1. Ensure `amazon_vacation_schedule.ods` exists and set its path in `config.yaml` under the `schedule_file` key.
2. Copy `config.toml.example` to `config.toml` and adjust the parameters as needed
3. Run the script using the following command:

   ```
   python main.py
   ```

   The script will perform calculations based on the provided parameters and generate a plot showing the PTO hours over time.
   
4. Review the output displayed in the terminal. It will show the PTO hours remaining at the end of the given period.

## Customization

Feel free to customize the script according to your specific needs. You can modify the parsing logic for the spreadsheet, adjust the parameters for different calculation periods, or modify the plot visualization.

## Contributing

Contributions to this project are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Make your changes or improvements.
3. Test your changes to ensure they work correctly.
4. Commit your changes and submit a pull request.

Please provide a clear description of the changes you have made and the problem they address. Your feedback and suggestions are also appreciated!

## License

This project is licensed under the [MIT License](LICENSE).

