use std::fs;
use std::io::{self, BufRead};

struct Reports {
    data: Vec<Vec<i32>>,
}

fn example_reports() -> Reports {
    Reports {
        data: vec![
            vec![7, 6, 4, 2, 1],
            vec![1, 2, 7, 8, 9],
            vec![9, 7, 6, 2, 1],
            vec![1, 3, 2, 4, 5],
            vec![8, 6, 4, 4, 1],
            vec![1, 3, 6, 7, 9],
        ],
    }
}

fn process_reports(reports: &Reports) -> usize {
    let mut safe_count = 0;
    let mut dampener_safe_count = 0;

    for report in &reports.data {
        if is_safe(report) {
            safe_count += 1;
        }
        if is_safe_with_dampener(report) {
            dampener_safe_count += 1;
        }
    }

    println!("Number of safe reports: {}", safe_count);
    println!(
        "Number of safe reports with dampener: {}",
        dampener_safe_count
    );
    safe_count & dampener_safe_count
}

// Function to check if report is safe
fn is_safe(report: &Vec<i32>) -> bool {
    let mut increasing = true;
    let mut decreasing = true;

    for i in 0..report.len() - 1 {
        let diff = report[i + 1] - report[i];
        let abs_diff = diff.abs();

        if abs_diff < 1 || abs_diff > 3 {
            return false;
        }
        if diff < 0 {
            increasing = false;
        }
        if diff > 0 {
            decreasing = false;
        }
    }
    increasing || decreasing
}

fn is_safe_with_dampener(report: &Vec<i32>) -> bool {
    if is_safe(report) {
        return true;
    }

    for i in 0..report.len() {
        let mut modified_report = report.clone();
        modified_report.remove(i);
        if is_safe(&modified_report) {
            return true;
        }
    }
    false
}

fn load_input_data(filename: &str) -> io::Result<Reports> {
    let file = fs::File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut data = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let report: Vec<i32> = line
            .split_whitespace()
            .filter_map(|num| num.parse::<i32>().ok())
            .collect();
        data.push(report);
    }
    Ok(Reports { data })
}

fn main() {
    let example_reports = example_reports();
    let reports = load_input_data("input.txt").expect("Failed to load input data");

    process_reports(&example_reports);
    process_reports(&reports);
}
