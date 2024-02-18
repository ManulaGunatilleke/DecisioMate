from h2o_wave import main, app, Q, ui
from rec_sys.prediction_handler import predict_price_range_from_input
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Initializing page...")

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        await init(q)
        q.client.initialized = True

    add_footer(q)

    await handle_form_submission(q)

    await q.page.save()

async def init(q: Q) -> None:
    logging.debug("Initializing page...")
    q.page['meta'] = ui.meta_card(box='', layouts=[ui.layout(breakpoint='xs', min_height='100vh', zones=[
        ui.zone('header'),
        ui.zone('content'),
        ui.zone('footer'),
    ])])
    q.page['header'] = ui.header_card(
        box='header', title='DecisioMate', subtitle="Let's Make Decision about Mobile Phones",
        image='https://wave.h2o.ai/img/h2o-logo.svg',
        secondary_items=[
            ui.tabs(name='tabs', value=f'#{q.args["#"]}' if q.args['#'] else '#page1', link=True, items=[
                ui.tab(name='#page1', label='Home'),
                ui.tab(name='#page2', label='Charts'),
                ui.tab(name='#page3', label='Grid'),
                ui.tab(name='#page4', label='Form'),
            ]),
        ],
        items=[
            ui.persona(title='Manula Gunatilleke', subtitle='Developer', size='xs',
                       image='#'),
        ]
    )
    await render_form(q)

    
# Sample data
sample_data = {
    'battery_power': 842,
    'blue': 0,
    'clock_speed': 2.2,
    'dual_sim': 0,
    'fc': 1,
    'four_g': 0,
    'int_memory': 7,
    'm_dep': 0.6,
    'mobile_wt': 188,
    'n_cores': 2,
    'pc': 2,
    'px_height': 20,
    'px_width': 756,
    'ram': 2549,
    'sc_h': 9,
    'sc_w': 7,
    'talk_time': 19,
    'three_g': 0,
    'touch_screen': 0,
    'wifi': 1,
    'price_range': 1,
}

# Render form with sample data
async def render_form(q: Q):
    logging.debug("Rendering form...")
    q.page['content'] = ui.form_card(box='content', items=[
        ui.textbox(name='battery_power', label='Battery Power', value=str(sample_data['battery_power'])),
        ui.textbox(name='blue', label='Blue', value=str(sample_data['blue'])),
        ui.textbox(name='clock_speed', label='Clock Speed', value=str(sample_data['clock_speed'])),
        ui.textbox(name='dual_sim', label='Dual Sim', value=str(sample_data['dual_sim'])),
        ui.textbox(name='fc', label='FC', value=str(sample_data['fc'])),
        ui.textbox(name='four_g', label='Four G', value=str(sample_data['four_g'])),
        ui.textbox(name='int_memory', label='Internal Memory', value=str(sample_data['int_memory'])),
        ui.textbox(name='m_dep', label='M Dep', value=str(sample_data['m_dep'])),
        ui.textbox(name='mobile_wt', label='Mobile Weight', value=str(sample_data['mobile_wt'])),
        ui.textbox(name='n_cores', label='N Cores', value=str(sample_data['n_cores'])),
        ui.textbox(name='pc', label='PC', value=str(sample_data['pc'])),
        ui.textbox(name='px_height', label='Px Height', value=str(sample_data['px_height'])),
        ui.textbox(name='px_width', label='Px Width', value=str(sample_data['px_width'])),
        ui.textbox(name='ram', label='RAM', value=str(sample_data['ram'])),
        ui.textbox(name='sc_h', label='SC H', value=str(sample_data['sc_h'])),
        ui.textbox(name='sc_w', label='SC W', value=str(sample_data['sc_w'])),
        ui.textbox(name='talk_time', label='Talk Time', value=str(sample_data['talk_time'])),
        ui.textbox(name='three_g', label='Three G', value=str(sample_data['three_g'])),
        ui.textbox(name='touch_screen', label='Touch Screen', value=str(sample_data['touch_screen'])),
        ui.textbox(name='wifi', label='WiFi', value=str(sample_data['wifi'])),
        ui.buttons(items=[ui.button(name='predict_button', label='Predict', primary=True)]),
    ])

async def handle_form_submission(q: Q):
    if q.args.predict_button:
        logging.debug("Handling form submission...")
        
        # Extract input values from the form
        battery_power = int(q.args.battery_power)
        blue = int(q.args.blue)
        clock_speed = float(q.args.clock_speed)
        dual_sim = int(q.args.dual_sim)
        fc = int(q.args.fc)
        four_g = int(q.args.four_g)
        int_memory = int(q.args.int_memory)
        m_dep = float(q.args.m_dep)
        mobile_wt = int(q.args.mobile_wt)
        n_cores = int(q.args.n_cores)
        pc = int(q.args.pc)
        px_height = int(q.args.px_height)
        px_width = int(q.args.px_width)
        ram = int(q.args.ram)
        sc_h = int(q.args.sc_h)
        sc_w = int(q.args.sc_w)
        talk_time = int(q.args.talk_time)
        three_g = int(q.args.three_g)
        touch_screen = int(q.args.touch_screen)
        wifi = int(q.args.wifi)
        # price_range = int(q.args.price_range)

        logging.debug("Input values: battery_power=%s, blue=%s, clock_speed=%s, dual_sim=%s, fc=%s, four_g=%s, int_memory=%s, m_dep=%s, mobile_wt=%s, n_cores=%s, pc=%s, px_height=%s, px_width=%s, ram=%s, sc_h=%s, sc_w=%s, talk_time=%s, three_g=%s, touch_screen=%s, wifi=%s,price_range=%s",
                      battery_power, blue, clock_speed, dual_sim, fc, four_g, int_memory, m_dep, mobile_wt, n_cores, pc, px_height, px_width, ram, sc_h, sc_w, talk_time, three_g, touch_screen, wifi)
        
        # Call prediction function
        predicted_price_range = predict_price_range_from_input(
            battery_power, blue, clock_speed, dual_sim, fc, four_g, int_memory, m_dep, mobile_wt, n_cores, pc, px_height, px_width, ram, sc_h, sc_w, talk_time, three_g, touch_screen, wifi
        )
        
        logging.debug("Predicted price range: %s", predicted_price_range)
        
        if predicted_price_range[0] == 0:
            prediction_text = 'You cannot sell this phone at a high price.'
        else:
            prediction_text = 'You can sell this phone at a high price.'

        q.page['content'] = ui.form_card(box='content', items=[
            ui.textbox(name='battery_power', label='Battery Power', value=str(battery_power)),
            ui.textbox(name='blue', label='Blue', value=str(blue)),
            ui.textbox(name='clock_speed', label='Clock Speed', value=str(clock_speed)),
            ui.textbox(name='dual_sim', label='Dual Sim', value=str(dual_sim)),
            ui.textbox(name='fc', label='FC', value=str(fc)),
            ui.textbox(name='four_g', label='Four G', value=str(four_g)),
            ui.textbox(name='int_memory', label='Internal Memory', value=str(int_memory)),
            ui.textbox(name='m_dep', label='M Dep', value=str(m_dep)),
            ui.textbox(name='mobile_wt', label='Mobile Weight', value=str(mobile_wt)),
            ui.textbox(name='n_cores', label='N Cores', value=str(n_cores)),
            ui.textbox(name='pc', label='PC', value=str(pc)),
            ui.textbox(name='px_height', label='Px Height', value=str(px_height)),
            ui.textbox(name='px_width', label='Px Width', value=str(px_width)),
            ui.textbox(name='ram', label='RAM', value=str(ram)),
            ui.textbox(name='sc_h', label='SC H', value=str(sc_h)),
            ui.textbox(name='sc_w', label='SC W', value=str(sc_w)),
            ui.textbox(name='talk_time', label='Talk Time', value=str(talk_time)),
            ui.textbox(name='three_g', label='Three G', value=str(three_g)),
            ui.textbox(name='touch_screen', label='Touch Screen', value=str(touch_screen)),
            ui.textbox(name='wifi', label='WiFi', value=str(wifi)),
            ui.textbox(name='predicted_price_range', label='Predicted Price Decision', value=prediction_text, disabled=True),
            ui.buttons(items=[ui.button(name='predict_button', label='Predict', primary=True)]),
        ])

        logging.debug("Form content updated.")

def add_footer(q: Q):
    caption = """__Made with 💛 by Manula Gunatilleke__ <br /> using __[h2o Wave](https://wave.h2o.ai/docs/getting-started).__"""
    q.page["footer"] = ui.footer_card(
        box="footer",
        caption=caption,
        items=[
            ui.inline(
                justify="end",
                items=[
                    ui.links(
                        label="Contact Me",
                        width="200px",
                        items=[
                            ui.link(
                                name="github",
                                label="GitHub",
                                path="https://github.com/ManulaGunatilleke",
                                target="_blank",
                            ),
                            ui.link(
                                name="linkedin",
                                label="LinkedIn",
                                path="https://www.linkedin.com/in/manula-gunatilleke/",
                                target="_blank",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

if __name__ == '__main__':
    main()
