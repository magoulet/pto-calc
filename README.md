# Amazon PTO Calculator

The Amazon PTO Calculator is a Python script designed to calculate and visualize the Paid Time Off (PTO) hours for Amazon corporate staff. It retrieves PTO data from an OpenDocument Spreadsheet (`amazon_vacation_schedule.ods`) and performs calculations based on the specified parameters. 

Please note that the following parameters should be adjusted in `main.py` as needed:

```python
filename = 'amazon_vacation_schedule.ods'
used = readTransactions(filename, 'baseline')
years = 4
months = 12
startMonth = 3
startYear  = 2021
```

The script requires the `amazon_vacation_schedule.ods` file to be located in the same directory as the main script. The spreadsheet should follow the schema:

```
tenure    end_date    year    month    vac    ppt    sick
0         1/31/2021   0       0
1         2/28/2021   0       1
2         3/31/2021   0       2
```

Where:
- `tenure` is the number of months
- `end_date` is the month-end date
- `year` is the year number
- `month` is the month number
- `vac`, `ppt`, and `sick` are the number of hours taken during the month

## Dependencies

This script requires the following dependencies to be installed:

- `matplotlib`
- `pandas`
- `python-odf`

To install the required dependencies, run the following command:

```
pip install matplotlib pandas odfpy
```

## Usage

To use the Amazon PTO Calculator, follow these steps:

1. Place the `amazon_vacation_schedule.ods` file in the same directory as the main script.
2. Open the `main.py` script in a text editor or IDE.
3. Adjust the parameters (`filename`, `years`, `months`, `startMonth`, `startYear`) as needed.
4. Run the script using the following command:

   ```
   python main.py
   ```

   The script will perform calculations based on the provided parameters and generate a plot showing the PTO hours over time.
   
5. Review the output displayed in the terminal. It will show the PTO hours remaining at the end of the given period.

The generated plot will be saved as `pto_plot.png` in the same directory.

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

