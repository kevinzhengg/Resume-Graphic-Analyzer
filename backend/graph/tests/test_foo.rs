use graphviz_rust::dot_generator::*;
use graphviz_rust::dot_structures::*;
use graphviz_rust::{exec, parse, cmd::Format,
                    printer::{DotPrinter, PrinterContext}};

#[cfg(test)]
mod tests {
    use super::*;


    #[test]
    pub fn test_create() {
    let mut g = graph!(strict di id!("asdasd");
                    node!("aa";attr!("color","green")),
                    subgraph!("v";node!("aa"; attr!("shape","square"))));


    // let dot_output = g.print(&mut PrinterContext::default());

    // log(&dot_output);

    let graph_svg = exec(g, &mut PrinterContext::default(), vec![Format::Svg.into()]).unwrap();

    let b = String::from_utf8(graph_svg.clone()).unwrap();

    assert_eq!(b, "asdasdj");
    }
}
