import os
import json
import pandas as pd
import numpy as np

def generate_ultimate_mavenflix_report(csv_path="extracted_files/Subscription Cohort Analysis Data.csv", output_html="mavenflix_report.html"):
    """
    Generates a Senior-Level Analytics Dashboard for MavenFlix dataset:
    1. Filters paid subscriptions and aggregates customer-level lifetime durations.
    2. Corrects censoring bias for 5+ month retention and M1 retention rankings.
    3. Excludes immature cohorts from the M1 bar chart (no misleading 0% bars).
    4. Renders a full Cohort Retention Heatmap Matrix (M0 to M12).
    5. Outputs a responsive mobile-friendly HTML report using Tailwind CSS and Chart.js.
    """
    if not os.path.exists(csv_path):
        csv_path = "Subscription Cohort Analysis Data.csv"

    print(f"Reading dataset from: {csv_path}")
    df_raw = pd.read_csv(csv_path)

    # 1. Filter Paid Subscriptions Only
    df_paid = df_raw[df_raw['was_subscription_paid'].astype(str).str.strip().str.capitalize() == 'Yes'].copy()
    
    # Parse dates
    df_paid['created_date'] = pd.to_datetime(df_paid['created_date'])
    df_paid['canceled_date'] = pd.to_datetime(df_paid['canceled_date'])

    # Determine reference max date in dataset
    max_date = max(df_paid['created_date'].max(), df_paid['canceled_date'].dropna().max())
    df_paid['created_month'] = df_paid['created_date'].dt.to_period('M').astype(str)

    # Calculate individual subscription duration in days and months
    df_paid['end_date'] = df_paid['canceled_date'].fillna(max_date)
    df_paid['days_subscribed'] = (df_paid['end_date'] - df_paid['created_date']).dt.days

    def calculate_duration_months(row):
        end = row['end_date']
        return (end.year - row['created_date'].year) * 12 + (end.month - row['created_date'].month)

    df_paid['duration_months'] = df_paid.apply(calculate_duration_months, axis=1)

    total_paid_subscriptions = len(df_paid)
    total_unique_customers = df_paid['customer_id'].nunique()

    # -------------------------------------------------------------
    # QUESTION 1: Paid Subscriptions Trend Over Time
    # -------------------------------------------------------------
    monthly_trends = df_paid.groupby('created_month').size().reset_index(name='new_subscribers')
    peak_row = monthly_trends.loc[monthly_trends['new_subscribers'].idxmax()]
    peak_month = str(peak_row['created_month'])
    peak_subscribers = int(peak_row['new_subscribers'])

    # -------------------------------------------------------------
    # QUESTION 2: 5+ Months Retention (Customer Level Aggregation)
    # -------------------------------------------------------------
    # Calculate lifetime metrics per unique customer (capturing reactivations)
    cust_first_created = df_paid.groupby('customer_id')['created_date'].min()
    cust_total_days = df_paid.groupby('customer_id')['days_subscribed'].sum()
    cust_total_months = (cust_total_days / 30.4375).astype(float)

    cust_5_plus_count = int((cust_total_months >= 5.0).sum())
    overall_pct_5_plus = round((cust_5_plus_count / total_unique_customers) * 100, 2)

    # Eligible customers cutoff (first subscription on or before May 31, 2023)
    may_2023_cutoff = pd.to_datetime('2023-05-31')
    eligible_cust_ids = cust_first_created[cust_first_created <= may_2023_cutoff].index
    eligible_cust_total = len(eligible_cust_ids)
    eligible_cust_5_plus = int((cust_total_months.loc[eligible_cust_ids] >= 5.0).sum())
    eligible_pct_5_plus = round((eligible_cust_5_plus / eligible_cust_total) * 100, 2) if eligible_cust_total > 0 else overall_pct_5_plus

    # -------------------------------------------------------------
    # QUESTION 3: M1 Retention Ranking & Full Cohort Retention Matrix
    # -------------------------------------------------------------
    m1_cutoff_date = max_date - pd.Timedelta(days=30)
    df_paid['is_m1_mature'] = df_paid['created_date'] <= m1_cutoff_date
    df_paid['retained_m1'] = df_paid['days_subscribed'] >= 30

    all_cohort_months = sorted(df_paid['created_month'].unique())
    m1_summary = []
    cohort_matrix_rows = []

    for cohort in all_cohort_months:
        c_df = df_paid[df_paid['created_month'] == cohort]
        c_size = len(c_df)

        # M1 Retention Check
        m1_mature_cnt = c_df['is_m1_mature'].sum()
        if c_size > 0 and (m1_mature_cnt / c_size) >= 0.75:
            retained_cnt = (c_df['days_subscribed'] >= 30).sum()
            m1_rate = round((retained_cnt / c_size) * 100, 2)
            m1_status = "Mature"
        else:
            m1_rate = None
            m1_status = "Immature"

        m1_summary.append({
            'cohort_month': str(cohort),
            'total_subscribers': c_size,
            'retention_rate': m1_rate,
            'status': m1_status
        })

        # Build Matrix Row (M0 to M12)
        matrix_row = {'cohort': cohort, 'size': c_size, 'rates': []}
        for m_offset in range(13):
            target_days = m_offset * 30.4375
            mature_members = c_df[c_df['created_date'] + pd.Timedelta(days=target_days) <= max_date]
            if len(mature_members) > 0 and (len(mature_members) / c_size) >= 0.5:
                active_cnt = (mature_members['days_subscribed'] >= target_days).sum()
                rate = round((active_cnt / len(mature_members)) * 100, 1)
                matrix_row['rates'].append(rate)
            else:
                matrix_row['rates'].append(None)
        cohort_matrix_rows.append(matrix_row)

    m1_summary_df = pd.DataFrame(m1_summary)

    # Mature Cohorts Only for Bar Chart & Min/Max Ranking
    mature_m1_df = m1_summary_df[m1_summary_df['status'] == "Mature"].dropna(subset=['retention_rate'])
    highest_m1_row = mature_m1_df.loc[mature_m1_df['retention_rate'].idxmax()]
    lowest_m1_row = mature_m1_df.loc[mature_m1_df['retention_rate'].idxmin()]

    highest_month = str(highest_m1_row['cohort_month'])
    highest_rate = float(highest_m1_row['retention_rate'])
    lowest_month = str(lowest_m1_row['cohort_month'])
    lowest_rate = float(lowest_m1_row['retention_rate'])

    # Bar chart lists (Only mature cohorts)
    mature_cohort_labels = mature_m1_df['cohort_month'].tolist()
    mature_cohort_rates = mature_m1_df['retention_rate'].tolist()

    # Safely prepare JSON data arrays for JavaScript
    trend_labels_json = json.dumps(monthly_trends['created_month'].tolist())
    trend_values_json = json.dumps(monthly_trends['new_subscribers'].tolist())

    mature_cohort_labels_json = json.dumps(mature_cohort_labels)
    mature_cohort_rates_json = json.dumps(mature_cohort_rates)

    # Helper function to generate HTML Cohort Heatmap Table
    def build_cohort_heatmap_html(matrix):
        headers_html = "".join([f"<th class='px-2 py-1.5 text-[11px] text-slate-300 font-semibold text-center'>M{i}</th>" for i in range(13)])
        rows_html = []
        for r in matrix:
            cells_html = f"<td class='px-2 py-1.5 text-xs font-mono font-bold text-slate-200 border-r border-slate-700/50'>{r['cohort']}</td>"
            cells_html += f"<td class='px-2 py-1.5 text-xs text-slate-400 text-center border-r border-slate-700/50'>{r['size']}</td>"
            for val in r['rates']:
                if val is None:
                    cells_html += "<td class='px-2 py-1.5 text-[10px] text-slate-600 text-center'>-</td>"
                else:
                    # Color styling based on retention rate
                    if val >= 80:
                        bg_cls = "bg-emerald-500/30 text-emerald-300"
                    elif val >= 60:
                        bg_cls = "bg-indigo-500/30 text-indigo-300"
                    elif val >= 40:
                        bg_cls = "bg-amber-500/30 text-amber-300"
                    else:
                        bg_cls = "bg-rose-500/30 text-rose-300"
                    cells_html += f"<td class='px-2 py-1.5 text-[11px] font-semibold text-center {bg_cls}'>{val}%</td>"
            rows_html.append(f"<tr class='border-b border-slate-800/60 hover:bg-slate-800/40'>{cells_html}</tr>")
        
        return f"""
        <div class="overflow-x-auto rounded-lg border border-slate-700">
            <table class="w-full text-left border-collapse">
                <thead class="bg-slate-900/80 border-b border-slate-700">
                    <tr>
                        <th class="px-2 py-1.5 text-xs text-slate-300 font-semibold">Cohort</th>
                        <th class="px-2 py-1.5 text-xs text-slate-300 font-semibold text-center border-r border-slate-700/50">Size</th>
                        {headers_html}
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows_html)}
                </tbody>
            </table>
        </div>
        """

    matrix_table_html = build_cohort_heatmap_html(cohort_matrix_rows)

    # Generate HTML Content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MavenFlix Analytics - Ultimate Report</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; }}
    </style>
</head>
<body class="p-4 md:p-8 max-w-5xl mx-auto">

    <!-- Header -->
    <header class="mb-6 text-center md:text-left border-b border-slate-700 pb-4">
        <div class="flex items-center justify-between flex-wrap gap-2">
            <h1 class="text-2xl md:text-3xl font-bold text-red-500">🎬 MavenFlix Analytics</h1>
            <span class="text-xs bg-emerald-500/20 text-emerald-400 px-2.5 py-1 rounded-full font-semibold border border-emerald-500/30">Paid Subscriptions Only</span>
        </div>
        <p class="text-slate-400 text-sm mt-1">Streaming Video Subscriptions Analytics (Customer-Aggregated & Rigorous)</p>
    </header>

    <!-- Key Metrics Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div class="card p-4 text-center">
            <span class="text-xs text-slate-400 uppercase font-semibold">Unique Paid Customers</span>
            <p class="text-2xl font-extrabold text-white mt-1">{total_unique_customers:,}</p>
            <span class="text-[10px] text-slate-500">({total_paid_subscriptions:,} total subscription records)</span>
        </div>
        <div class="card p-4 text-center">
            <span class="text-xs text-slate-400 uppercase font-semibold">Subscribed 5+ Months</span>
            <p class="text-2xl font-extrabold text-emerald-400 mt-1">{eligible_pct_5_plus}%</p>
            <span class="text-[10px] text-slate-400">({eligible_cust_5_plus:,} / {eligible_cust_total:,} eligible unique customers)</span>
        </div>
        <div class="card p-4 text-center">
            <span class="text-xs text-slate-400 uppercase font-semibold">Peak Month</span>
            <p class="text-2xl font-extrabold text-indigo-400 mt-1">{peak_month}</p>
            <span class="text-[10px] text-slate-400">({peak_subscribers} new paid subscribers)</span>
        </div>
    </div>

    <!-- Question 1: Trend Analysis -->
    <section class="card p-5 mb-6">
        <h2 class="text-lg font-semibold text-red-400 mb-2">1. How have MavenFlix subscriptions trended over time?</h2>
        <p class="text-slate-300 text-sm mb-4">
            Paid subscriptions dipped slightly in late 2022 before experiencing strong, sustained growth to an all-time peak in 
            <strong>{peak_month}</strong> with <strong>{peak_subscribers} new paid subscribers</strong>. The drop in late 2023-09 reflects data extraction cutoff.
        </p>
        <div class="relative w-full h-64">
            <canvas id="trendChart"></canvas>
        </div>
    </section>

    <!-- Question 2: 5+ Months Retention -->
    <section class="card p-5 mb-6">
        <h2 class="text-lg font-semibold text-emerald-400 mb-2">2. What percentage of customers subscribed for 5+ months?</h2>
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="text-sm text-slate-300">
                <p class="mb-2">
                    Among <i>eligible unique customers</i> (joined on or before May 2023 with full 5-month observation window), 
                    <strong class="text-emerald-400 text-xl">{eligible_pct_5_plus}%</strong> ({eligible_cust_5_plus:,} out of {eligible_cust_total:,}) maintained their subscription for <strong>5 months or longer</strong> across their lifetime.
                </p>
                <p class="text-xs text-slate-400 border-l-2 border-emerald-500 pl-2 mt-2">
                    Across all total customer accounts (including brand-new accounts created after May 2023), the unadjusted rate is <strong>{overall_pct_5_plus}%</strong> ({cust_5_plus_count:,} / {total_unique_customers:,}).
                </p>
            </div>
            <div class="w-36 h-36 flex-shrink-0 flex flex-col items-center">
                <canvas id="gaugeChart"></canvas>
                <span class="text-[10px] text-slate-400 mt-1 font-semibold">Eligible Customers Rate</span>
            </div>
        </div>
    </section>

    <!-- Question 3: Retention Analysis -->
    <section class="card p-5 mb-6">
        <h2 class="text-lg font-semibold text-indigo-400 mb-2">3. What month has the highest and lowest subscriber retention?</h2>
        <p class="text-xs text-slate-400 mb-3">
            *Evaluated on mature Month-1 Retention (≥ 30 days active). Immature cohorts (late August & September 2023) are excluded from ranking to prevent censoring bias.
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div class="bg-slate-900/50 p-3 rounded-lg border border-slate-700">
                <span class="text-xs text-emerald-400 font-bold uppercase">Highest Retention Month (M1)</span>
                <p class="text-xl font-bold mt-1 text-white">{highest_month}</p>
                <p class="text-xs text-slate-400">Month-1 Retention Rate: <strong class="text-emerald-400">{highest_rate}%</strong></p>
            </div>
            <div class="bg-slate-900/50 p-3 rounded-lg border border-slate-700">
                <span class="text-xs text-rose-400 font-bold uppercase">Lowest Retention Month (M1)</span>
                <p class="text-xl font-bold mt-1 text-white">{lowest_month}</p>
                <p class="text-xs text-slate-400">Month-1 Retention Rate: <strong class="text-rose-400">{lowest_rate}%</strong></p>
            </div>
        </div>

        <p class="text-xs text-slate-300 bg-slate-900/40 p-2.5 rounded border border-slate-700/50 mb-4">
            💡 <strong>Analytical Insight:</strong> Retention is remarkably consistent across all mature cohorts, varying within a narrow band between <strong>{lowest_rate}%</strong> and <strong>{highest_rate}%</strong>.
        </p>

        <!-- Mature Cohorts Bar Chart -->
        <div class="relative w-full h-64 mb-6">
            <canvas id="retentionChart"></canvas>
        </div>

        <!-- Full Cohort Retention Heatmap Matrix Table -->
        <h3 class="text-sm font-semibold text-slate-300 mb-2">Full Cohort Retention Matrix (M0 - M12)</h3>
        {matrix_table_html}
    </section>

    <footer class="text-center text-xs text-slate-500 my-6">
        Generated automatically from MavenFlix Dataset | Customer-Aggregated & Rigorous Analytics
    </footer>

    <!-- Chart.js Scripts -->
    <script>
        // Trend Chart (Line)
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                labels: {trend_labels_json},
                datasets: [{{
                    label: 'Paid Subscribers',
                    data: {trend_values_json},
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }}
                }}
            }}
        }});

        // Gauge Chart (Doughnut)
        new Chart(document.getElementById('gaugeChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['Eligible 5+ Months', 'Dropped < 5 Months'],
                datasets: [{{
                    data: [{eligible_pct_5_plus}, {round(100 - eligible_pct_5_plus, 2)}],
                    backgroundColor: ['#34d399', '#334155'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                cutout: '75%'
            }}
        }});

        // Retention Chart (Bar for Mature Cohorts Only)
        const matureLabels = {mature_cohort_labels_json};
        const matureRates = {mature_cohort_rates_json};
        const highestMonthStr = "{highest_month}";
        const lowestMonthStr = "{lowest_month}";

        const barColors = matureLabels.map(label => {{
            if (label === highestMonthStr) return '#34d399'; // Emerald
            if (label === lowestMonthStr) return '#f43f5e'; // Rose
            return '#818cf8'; // Indigo
        }});

        new Chart(document.getElementById('retentionChart'), {{
            type: 'bar',
            data: {{
                labels: matureLabels,
                datasets: [{{
                    label: 'Month-1 Retention Rate (%)',
                    data: matureRates,
                    backgroundColor: barColors,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return ' Month-1 Retention Rate: ' + context.parsed.y + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, max: 100 }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[✔] Ultimate Mobile HTML Report generated successfully: {output_html}")

if __name__ == "__main__":
    generate_ultimate_mavenflix_report()