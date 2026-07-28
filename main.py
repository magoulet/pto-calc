import datetime as dt
import logging
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from pto_classes import FlexiblePTO, StandardPTO

logger = logging.getLogger(__name__)


def read_schedule(filename, sheetName):
    df = pd.read_excel(filename, 
                       engine="odf", 
                       sheet_name=sheetName,
                       usecols='A:C', 
                       parse_dates=['end_date'],
                       )
    
    df['flexible'] = pd.to_numeric(df['flexible'], errors='coerce')
    df['standard'] = pd.to_numeric(df['standard'], errors='coerce')
    return df


def plot_pto_results(results: pd.DataFrame, save_path: Path = None) -> go.Figure:
    """
    Create an interactive plot of PTO results using plotly.
    
    Args:
        results (pd.DataFrame): DataFrame containing PTO data with columns:
            'periodEnd', 'Total Days', 'Flexible', 'Standard', 'Flexible Lost', 'Std Lost'
        save_path (Path, optional): Path to save the plot. Defaults to None.
    
    Returns:
        go.Figure: Plotly figure object
    """
    
    # Create figure
    fig = go.Figure()

    # Add traces
    # Total Days line
    fig.add_trace(
        go.Scatter(
            x=results['periodEnd'],
            y=results['Total Days'],
            mode='lines+markers',
            name='PTO'
        )
    )

    # Add stacked area plots for Flexible and Standard
    fig.add_trace(
        go.Scatter(
            x=results['periodEnd'],
            y=results['Flexible']/8,
            name='Flexible',
            fill='tonexty',
            stackgroup='one'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=results['periodEnd'],
            y=results['Standard']/8,
            name='Standard',
            fill='tonexty',
            stackgroup='one'
        )
    )

    # Add stacked area plots for Lost hours
    fig.add_trace(
        go.Scatter(
            x=results['periodEnd'],
            y=results['Flexible Lost']/8,
            name='Lost (Flexible)',
            fill='tonexty',
            stackgroup='two',
            line=dict(color='red')
        )
    )

    fig.add_trace(
        go.Scatter(
            x=results['periodEnd'],
            y=results['Std Lost']/8,
            name='Lost (Std)',
            fill='tonexty',
            stackgroup='two',
            line=dict(color='blue')
        )
    )

    # Add vertical line for today
    fig.add_vline(
        x=dt.date.today(),
        line_dash="dash",
        line_color="red"
    )

    # Update layout
    fig.update_layout(
        title='Paid Time Off (days)',
        xaxis_title='Period End Date',
        yaxis_title='Days',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        width=1000,
        height=500,
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        hovermode='x unified'
    )

    # Customize hover template
    fig.update_traces(
        hovertemplate='Date: %{x}<br>Days: %{y:.1f}<extra></extra>'
    )

    # Save if path provided
    if save_path:
        if save_path.suffix == '.html':
            fig.write_html(save_path)
        else:
            fig.write_image(save_path)

    return fig

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

    from config_loader import config
    flexible = FlexiblePTO(config.model_dump())
    standard = StandardPTO(config.model_dump())

    filename = config.schedule_file
    schedule = read_schedule(filename, 'baseline')

    data = []

    for row in schedule.itertuples():
        flexible.use(row.flexible, row.end_date)
        standard.use(row.standard, row.end_date)

        flexible.forward(row.end_date)
        standard.forward(row.end_date)

        data.append([
            row.end_date, 
            flexible.bal, 
            standard.bal, 
            flexible.lost,
            standard.lost, 
            sum([flexible.bal, standard.bal])/8
            ])

    results = pd.DataFrame(data)
    results.columns=[
        'periodEnd', 
        'Flexible', 
        'Standard', 
        'Flexible Lost', 
        'Std Lost', 
        'Total Days',
        ]
    print("PTO hours left over at end of given period\n")
    print(results)

    fig = plot_pto_results(results)
    fig.show()
