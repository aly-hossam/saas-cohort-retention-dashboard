# Data Inspection & Overview Report

**Root Directory:** `/root/Desktop/Project_3`

---

## Dataset: `extracted_files/Subscription Cohort Analysis Data Dictionary.csv`

### 1. General Info
- **Total Rows:** `6`
- **Total Columns:** `2`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `Field` | `object` | 6 | 0 | 0.00% | 6 | customer_id |
| `Description` | `object` | 6 | 0 | 0.00% | 6 | Unique customer identificat... |


### 4. Data Preview (Head 5 Rows)
| Field | Description |
| --- | --- |
| customer_id | Unique customer identification number representing an individual customer |
| created_date | Date the customer subscription was created (MM/DD/YYYY) |
| canceled_date | Date the customer subscription was canceled (MM/DD/YYYY). If value is blank then the subscription has not been canceled |
| subscription_cost | Price of the subscription in USD |
| subscription_interval | Measurement of time between billing occurrences for a recurring billing subscription |

---

## Dataset: `extracted_files/Subscription Cohort Analysis Data.csv`

### 1. General Info
- **Total Rows:** `3,069`
- **Total Columns:** `6`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `customer_id` | `int64` | 3,069 | 0 | 0.00% | 2,877 | 154536156 |
| `created_date` | `object` | 3,069 | 0 | 0.00% | 370 | 2022-09-01 |
| `canceled_date` | `object` | 2,004 | 1,065 | 34.70% | 360 | 2022-09-02 |
| `subscription_cost` | `int64` | 3,069 | 0 | 0.00% | 1 | 39 |
| `subscription_interval` | `object` | 3,069 | 0 | 0.00% | 1 | month |
| `was_subscription_paid` | `object` | 3,069 | 0 | 0.00% | 2 | Yes |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| customer_id | 111394466.0 | 155926313.0 | 184143564.0 | 214248197.0 | 221189604.0 | 182755333.71098077 | 30078626.71775289 |
| subscription_cost | 39.0 | 39.0 | 39.0 | 39.0 | 39.0 | 39.0 | 0.0 |


### 4. Data Preview (Head 5 Rows)
| customer_id | created_date | canceled_date | subscription_cost | subscription_interval | was_subscription_paid |
| --- | --- | --- | --- | --- | --- |
| 154536156 | 2022-09-01 | nan | 39 | month | Yes |
| 149713408 | 2022-09-01 | 2022-09-02 | 39 | month | No |
| 153756284 | 2022-09-01 | 2022-09-02 | 39 | month | No |
| 121253113 | 2022-09-01 | 2022-09-23 | 39 | month | Yes |
| 154467210 | 2022-09-01 | 2023-06-29 | 39 | month | Yes |

---
