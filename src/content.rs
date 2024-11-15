use std::borrow::ToOwned;
use std::collections::HashMap;
use std::fs;
use egui_commonmark::{commonmark_str, CommonMarkCache};
use wasm_bindgen_futures::wasm_bindgen::prelude::wasm_bindgen;

pub const CONTENT_PATH: &str = "assets/content/";

#[derive(serde::Deserialize, serde::Serialize)]
pub struct Tab {
    #[serde(skip)]
    pub cache: CommonMarkCache,
    pub path: String,
}

impl Tab {
    pub fn new(filename: &str) -> Self {
        let cache = CommonMarkCache::default();
        // commonmark_str!(CONTENT_PATH.clone().to_owned() + filename).expect("Error!");

        Self {
            cache,
            path: filename.parse().unwrap(),
        }
    }
}

pub fn  load_tabs() -> Vec<Tab> {
    let mut tabs = Vec::new();

    tabs.push(Tab::new("test.md"));

    tabs
}

// pub const TABS: Vec<Tab> = load_tabs();

// pub fn load_tabs() -> Vec<Tab> {
//
//     let paths = fs::read_dir("./").unwrap();
//
//     let mut tabs: Vec<Tab> = Vec::new();
//     //
//     for path in paths {
//         if !path.is_ok() {continue;}
//         let str_path = path.unwrap().path().to_str().unwrap().to_owned();
//         tabs[0] = Tab {
//             cache: CommonMarkCache::default(),
//             content: fs::read_to_string(&str_path).expect("Error!"),
//             path: str_path,
//         }
//     }
//
//     tabs
//
//
// }