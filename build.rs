// build.rs

use std::env;
use std::fs;
use std::path::Path;

fn main() {
    let out_dir = env::var_os("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("page-loader.rs");

    let paths = fs::read_dir("assets/content/").unwrap();

    // let mut tabs: HashMap<String, String> = HashMap::new();

    let mut new_file = r#"
use lazy_static::lazy_static;
use std::collections::HashMap;
use egui_commonmark::{commonmark};

//pub const cache: CommonMarkCache = CommonMarkCache::default();

pub fn get_page(index: usize, ui: &mut egui::Ui, cache: &mut CommonMarkCache) {
    match index {
"#.to_owned();

    let mut files = "[".to_owned();

    for (i, path) in paths.enumerate() {
        if !path.is_ok() {continue;}
        let file = path.unwrap();
        if file.file_type().unwrap().is_dir() {continue;}

        let path = file.path().to_str().unwrap().to_owned();
        let filename = file.file_name().to_str().unwrap().to_owned();

        // new_file += format!(r#"("{}", {}),"#, filename, "r#\"".to_owned() + &fs::read_to_string(path).expect("# ERROR!") + "\"#").as_str();
//         new_file += format!(r#"
// {} => {},"#, i, "{commonmark!(ui, cache, \"".to_owned() + &*fs::read_to_string(path).expect("# ERROR!")+ "\");}").as_str();
        new_file += format!(r#"
{} => {},"#, i, "{commonmark_str!(ui, cache, \"".to_owned()+&*path+"\");}").as_str();

        files += ({if i != 0 {","} else {""}}.to_owned() + "\"" + &*filename + "\"").as_str();

        // tabs.insert(filename.clone(), fs::read_to_string(path).expect("# ERROR!"));
    }

    // files += "]";

    new_file += r#"
_ => {commonmark!(ui, cache, "File does not exist");}}}"#;


    new_file += format!(r#"

pub const PAGE_FILES: &'static [&'static str] = &{}];"#, files).as_str();

    fs::write(&dest_path, new_file).unwrap();

    // println!("{}", new_file);

    // fs::read_to_string("/ee").unwrap();

    println!("cargo::rerun-if-changed=build.rs");
}