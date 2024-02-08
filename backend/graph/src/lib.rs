mod utils;

use wasm_bindgen::prelude::*;
use cfg_if::cfg_if;
use graphviz_rust::dot_generator::*;
use graphviz_rust::dot_structures::*;
use graphviz_rust::{exec, parse, cmd::Format,
                    printer::{DotPrinter, PrinterContext}};

cfg_if! {
    if #[cfg(feature = "wee_alloc")] {
        #[global_allocator]
        static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;
    }
}


#[wasm_bindgen]
pub fn test_create(name: &str) {
    let mut g = graph!(strict di id!(name);
                    node!("aa";attr!("color","green")),
                    subgraph!("v";node!("aa"; attr!("shape","square"))));


    let dot_output = g.print(&mut PrinterContext::default());

    log(&dot_output);

    let graph_svg = exec(g, &mut PrinterContext::default(), vec![Format::Svg.into()]).unwrap();
    let b = String::from_utf8(graph_svg.clone()).unwrap();
    log(&b);
}


#[wasm_bindgen]
extern "C" {
    pub fn alert(s: &str);

    // console.log for str
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);


    #[wasm_bindgen(js_namespace = console, js_name = log)]
    fn log_arr(a: Vec<u8>);
}


#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}", name));
}


