use regex::Regex;
use std::fs;

struct Instruction {
    data: Vec<String>,
}

fn example_instruction_1() -> Instruction {
    Instruction {
        data: vec![String::from(
            "xmul(2,4)%&mul[3,7]!@^don't()mul(5,5)+do()mul(32,64]then(mul(11,8)mul(8,5))",
        )],
    }
}

fn example_instruction_2() -> Instruction {
    Instruction {
        data: vec![String::from(
            "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
        )],
    }
}

fn real_instruction() -> Instruction {
    let input = fs::read_to_string("input.txt").expect("Failed to read input.txt");
    Instruction { data: vec![input] }
}

fn index_dos_donts(instruction: &Instruction) -> Vec<(usize, usize, bool)> {
    let do_re = Regex::new(r"do\(\)").unwrap();
    let dont_re = Regex::new(r"don't\(\)").unwrap();

    let mut indices = Vec::new();

    for line in &instruction.data {
        for mat in do_re.find_iter(line) {
            indices.push((mat.start(), mat.end(), true));
        }
        for mat in dont_re.find_iter(line) {
            indices.push((mat.start(), mat.end(), false));
        }
    }

    indices.sort_by_key(|&(start, _, _)| start);
    indices
}

fn combine_do_sections(input: &str, indices: &[(usize, usize, bool)]) -> String {
    let mut result = String::new();
    let mut is_enabled = true;
    let mut current_index = 0;

    for &(start, end, is_do) in indices {
        if is_enabled {
            result.push_str(&input[current_index..start]);
        }
        is_enabled = is_do;
        current_index = end;
    }

    if is_enabled {
        result.push_str(&input[current_index..]);
    }

    result
}

fn process_instruction(instruction: &Instruction) {
    let mul_re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();

    for line in &instruction.data {
        let indices = index_dos_donts(&Instruction {
            data: vec![line.clone()],
        });

        let filtered_input = combine_do_sections(line, &indices);

        let mut sum = 0;
        for caps in mul_re.captures_iter(&filtered_input) {
            let x: i32 = caps[1].parse().unwrap();
            let y: i32 = caps[2].parse().unwrap();
            sum += x * y;
        }

        println!("Sum of valid multiplications: {}", sum);
    }
}

fn main() {
    println!("Processing example instruction 1:");
    let example_1 = example_instruction_1();
    process_instruction(&example_1);

    println!("Processing example instruction 2:");
    let example_2 = example_instruction_2();
    process_instruction(&example_2);

    println!("\nProcessing real instructions from input.txt:");
    let real = real_instruction();
    process_instruction(&real);
}
