use egui::{Color32, FontFamily, Frame, Theme, Visuals};
use egui_commonmark::{CommonMarkCache, CommonMarkViewer};

const MD: &str = r#"
# **H1!**
## H2!
### H3!
[LINK](https://astatin3.dev)
"#;

#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)]
pub struct App {
    #[serde(skip)]
    common_mark_cache: CommonMarkCache,
}

impl App {
    pub fn name() -> &'static str {
        "TEST APP"
    }
}

impl Default for App {
    fn default() -> Self {
        Self {
            common_mark_cache: CommonMarkCache::default()
        }
    }
}

impl eframe::App for App {
    // fn save(&mut self, storage: &mut dyn eframe::Storage) {
    //     eframe::set_value(storage, eframe::APP_KEY, self);
    // }
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {

        let frame = Frame {
            fill: {
                if ctx.system_theme().unwrap() == Theme::Dark  {
                    Color32::from_rgb(64,64,64)
                } else {
                    Color32::from_rgb(144,144,144)
                }
            },
            ..Default::default()
        };

        egui::CentralPanel::default().frame(Frame::none()).show(ctx, |ui| {
            ui.style_mut().url_in_tooltip = true;


            egui::TopBottomPanel::top("BAR").show(ctx, |ui| {
                egui::menu::bar(ui, |ui| {
                    egui::widgets::global_theme_preference_switch(ui);
                    let _ = ui.colored_label(Color32::GREEN, "ASTATIN3.dev");
                });
            });

            egui::ScrollArea::vertical().show(ui, |ui| {
                CommonMarkViewer::new().show_scrollable("viewer", ui, &mut self.common_mark_cache, MD);
                // let painter = ui.painter();
                // painter.rect(egui::Rect {min:egui::Pos2{x: 0., y: 0.},max:egui::Pos2{x: 100., y: 100.}}, 0., Color32::WHITE, egui::Stroke::NONE);
            });
        });
    }

}