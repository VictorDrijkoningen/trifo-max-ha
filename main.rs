use std::io::Read;

use serde::Deserialize;


fn main() {
    // Open the file
    let mut file = std::fs::File::open("config_mono_auto_tasks.json.sample").expect("Failed to open file");

    // Read the file content into a string
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Failed to read file");

    // Deserialize the JSON data into a `serde_json::Value`
    let data: serde_json::Value = serde_json::from_str(&contents).expect("Failed to parse JSON");

    // Print the parsed data
    println!("{:?}", data);

    // Example of accessing a specific value in the JSON
    if let Some(data) = data.get("data") {
        println!("data: {}", data);
    }
}