#include "emptyvia.hpp"
#include "via_module.hpp"

// Add module to:
// starling.cpp
// starling.hpp
// plugin.json
// to build and run

// Add SVG to res or customize blank.svg for panel art

#define EMPTYVIA_OVERSAMPLE_AMOUNT 1

struct Emptyvia : Via<EMPTYVIA_OVERSAMPLE_AMOUNT, 0> {

    enum ParamIds {
        KNOB1_PARAM,
        KNOB2_PARAM,
        KNOB3_PARAM,
        A_PARAM,
        B_PARAM,
        CV2AMT_PARAM,
        CV3AMT_PARAM,
        BUTTON1_PARAM,
        BUTTON2_PARAM,
        BUTTON3_PARAM,
        BUTTON4_PARAM,
        BUTTON5_PARAM,
        BUTTON6_PARAM,
        TRIGBUTTON_PARAM,
        NUM_PARAMS
    };
    enum InputIds {
        A_INPUT,
        B_INPUT,
        CV1_INPUT,
        CV2_INPUT,
        CV3_INPUT,
        MAIN_LOGIC_INPUT,
        AUX_LOGIC_INPUT,
        NUM_INPUTS
    };
    enum OutputIds {
        MAIN_OUTPUT,
        LOGICA_OUTPUT,
        AUX_DAC_OUTPUT,
        AUX_LOGIC_OUTPUT,
        NUM_OUTPUTS
    };
    enum LightIds {
        LED1_LIGHT,
        LED2_LIGHT,
        LED3_LIGHT,
        LED4_LIGHT,
        OUTPUT_GREEN_LIGHT,
        OUTPUT_RED_LIGHT,
        RED_LIGHT,
        GREEN_LIGHT,
        BLUE_LIGHT,
        PURPLE_LIGHT,
        NUM_LIGHTS
    };
    
    Emptyvia() : Via() {

        virtualIO = &virtualModule;

        config(NUM_PARAMS, NUM_INPUTS, NUM_OUTPUTS, NUM_LIGHTS);
        configParam(KNOB1_PARAM, 0, 4095.0, 2048.0, "Label Me!");
        configParam(KNOB2_PARAM, 0, 4095.0, 2048.0, "Label Me!");
        configParam(KNOB3_PARAM, 0, 4095.0, 2048.0, "Label Me!");
        configParam(B_PARAM, -1.0, 1.0, 0.5, "Label Me!");
        configParam(CV2AMT_PARAM, 0, 1.0, 1.0, "Label Me!");
        configParam(A_PARAM, -5.0, 5.0, 5.0, "Label Me!");
        configParam(CV3AMT_PARAM, 0, 1.0, 1.0, "Label Me!");
        
        configParam(BUTTON1_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        configParam(BUTTON2_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        configParam(BUTTON3_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        configParam(BUTTON4_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        configParam(BUTTON5_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        configParam(BUTTON6_PARAM, 0.0, 1.0, 0.0, "Label Me!");
        
        configParam(TRIGBUTTON_PARAM, 0.0, 5.0, 0.0, "Label Me!");

        onSampleRateChange();

    }
    void process(const ProcessArgs &args) override;

    ViaEmptyvia virtualModule;

    void onSampleRateChange() override {
        float sampleRate = APP->engine->getSampleRate();

        ledDecay = 1.0/sampleRate;

        if (sampleRate == 44100.0) {
            divideAmount = 1;
        } else if (sampleRate == 48000.0) {
            divideAmount = 1;
        } else if (sampleRate == 88200.0) {
            divideAmount = 2;
        } else if (sampleRate == 96000.0) {
            divideAmount = 2;
        } else if (sampleRate == 176400.0) {
            divideAmount = 4;
        } else if (sampleRate == 192000.0) {
            divideAmount = 4;
        } else if (sampleRate == 352800.0) {
            divideAmount = 8;
        } else if (sampleRate == 384000.0) {
            divideAmount = 8;
        } else if (sampleRate == 705600.0) {
            divideAmount = 16;
        } else if (sampleRate == 768000.0) {
            divideAmount = 16;
        }
        
    }

    json_t *dataToJson() override {

        json_t *rootJ = json_object();

        json_object_set_new(rootJ, "modes", json_integer(virtualModule.oscUI.modeStateBuffer));
        
        return rootJ;
    }
    
    void dataFromJson(json_t *rootJ) override {

        json_t *modesJ = json_object_get(rootJ, "modes");
        virtualModule.oscUI.modeStateBuffer = json_integer_value(modesJ);
        virtualModule.oscUI.loadFromEEPROM(0);
        virtualModule.oscUI.recallModuleState();


    }
    
};

void Emptyvia::process(const ProcessArgs &args) {

    clockDivider++;

    if (clockDivider >= divideAmount) {

        // update the "slow IO" (not audio rate) every 16 samples
        // needs to scale with sample rate somehow
        slowIOPrescaler++;
        if (slowIOPrescaler == 16) {
            slowIOPrescaler = 0;
            updateSlowIO();
            virtualModule.slowConversionCallback();
            virtualModule.ui_dispatch(SENSOR_EVENT_SIG);
            virtualModule.oscUI.incrementTimer();
            processTriggerButton();
            updateLEDs();
        }

        updateAudioRate();

    }
    
}

struct EmptyviaWidget : ModuleWidget  {

    EmptyviaWidget(Emptyvia *module) {

	box.size = Vec(12 * RACK_GRID_WIDTH, RACK_GRID_HEIGHT);

        // EDIT TO CHANGE PANEL
        setPanel(APP->window->loadSvg(asset::plugin(pluginInstance, "res/blank.svg")));

        setModule(module);

        addChild(createWidget<ScrewSilver>(Vec(RACK_GRID_WIDTH, 0)));
        addChild(createWidget<ScrewSilver>(Vec(box.size.x - 2 * RACK_GRID_WIDTH, 0)));
        addChild(createWidget<ScrewSilver>(Vec(RACK_GRID_WIDTH, RACK_GRID_HEIGHT - RACK_GRID_WIDTH)));
        addChild(createWidget<ScrewSilver>(Vec(box.size.x - 2 * RACK_GRID_WIDTH, RACK_GRID_HEIGHT - RACK_GRID_WIDTH)));

        addParam(createParam<ViaSifamBlack>(Vec(9.022 + .753, 30.90), module, Emptyvia::KNOB1_PARAM));
        addParam(createParam<ViaSifamBlack>(Vec(68.53 + .753, 30.90), module, Emptyvia::KNOB2_PARAM));
        addParam(createParam<ViaSifamBlack>(Vec(68.53 + .753, 169.89), module, Emptyvia::KNOB3_PARAM));
        addParam(createParam<ViaSifamGrey>(Vec(9.022 + .753, 169.89), module, Emptyvia::B_PARAM));
        addParam(createParam<ViaSifamBlack>(Vec(128.04 + .753, 30.90), module, Emptyvia::CV2AMT_PARAM));
        addParam(createParam<ViaSifamGrey>(Vec(128.04 + .753, 100.4), module, Emptyvia::A_PARAM));
        addParam(createParam<ViaSifamBlack>(Vec(128.04 + .753, 169.89), module, Emptyvia::CV3AMT_PARAM));
        
        addParam(createParam<TransparentButton>(Vec(10.5 + .753, 80), module, Emptyvia::BUTTON1_PARAM));
        addParam(createParam<TransparentButton>(Vec(47 + .753, 77.5), module, Emptyvia::BUTTON2_PARAM));
        addParam(createParam<TransparentButton>(Vec(85 + .753, 80), module, Emptyvia::BUTTON3_PARAM));
        addParam(createParam<TransparentButton>(Vec(10.5 + .753, 129), module, Emptyvia::BUTTON4_PARAM));
        addParam(createParam<TransparentButton>(Vec(46 + .753, 131.5), module, Emptyvia::BUTTON5_PARAM));
        addParam(createParam<TransparentButton>(Vec(85 + .753, 129), module, Emptyvia::BUTTON6_PARAM));
        
        addParam(createParam<ViaPushButton>(Vec(132.7 + .753, 320), module, Emptyvia::TRIGBUTTON_PARAM));

        addInput(createInput<ViaJack>(Vec(8.07 + 1.053, 241.12), module, Emptyvia::A_INPUT));
        addInput(createInput<ViaJack>(Vec(8.07 + 1.053, 282.62), module, Emptyvia::B_INPUT));
        addInput(createInput<ViaJack>(Vec(8.07 + 1.053, 324.02), module, Emptyvia::MAIN_LOGIC_INPUT));
        addInput(createInput<ViaJack>(Vec(45.75 + 1.053, 241.12), module, Emptyvia::CV1_INPUT));
        addInput(createInput<ViaJack>(Vec(45.75 + 1.053, 282.62), module, Emptyvia::CV2_INPUT));
        addInput(createInput<ViaJack>(Vec(45.75 + 1.053, 324.02), module, Emptyvia::CV3_INPUT));
        addInput(createInput<ViaJack>(Vec(135 + 1.053, 282.62), module, Emptyvia::AUX_LOGIC_INPUT));

        addOutput(createOutput<ViaJack>(Vec(83.68 + 1.053, 241.12), module, Emptyvia::LOGICA_OUTPUT));
        addOutput(createOutput<ViaJack>(Vec(83.68 + 1.053, 282.62), module, Emptyvia::AUX_DAC_OUTPUT));
        addOutput(createOutput<ViaJack>(Vec(83.68 + 1.053, 324.02), module, Emptyvia::MAIN_OUTPUT));
        addOutput(createOutput<ViaJack>(Vec(135 + 1.053, 241.12), module, Emptyvia::AUX_LOGIC_OUTPUT));

        addChild(createLight<MediumLight<WhiteLight>>(Vec(35.8 + .753, 268.5), module, Emptyvia::LED1_LIGHT));
        addChild(createLight<MediumLight<WhiteLight>>(Vec(73.1 + .753, 268.5), module, Emptyvia::LED2_LIGHT));
        addChild(createLight<MediumLight<WhiteLight>>(Vec(35.8 + .753, 309.9), module, Emptyvia::LED3_LIGHT));
        addChild(createLight<MediumLight<WhiteLight>>(Vec(73.1 + .753, 309.9), module, Emptyvia::LED4_LIGHT));
        addChild(createLight<MediumLight<GreenRedLight>>(Vec(54.8 + .753, 179.6), module, Emptyvia::OUTPUT_GREEN_LIGHT));
        addChild(createLight<LargeLight<RGBTriangle>>(Vec(59 + .753, 221), module, Emptyvia::RED_LIGHT));

    };

    void appendContextMenu(Menu *menu) override {
        // Emptyvia *module = dynamic_cast<Emptyvia*>(this->module);

        struct PresetRecallItem : MenuItem {
            Emptyvia *module;
            int preset;
            void onAction(const event::Action &e) override {
                module->virtualModule.oscUI.modeStateBuffer = preset;
                module->virtualModule.oscUI.loadFromEEPROM(0);
                module->virtualModule.oscUI.recallModuleState();
            }
        };

    }
    
};

Model *modelEmptyvia = createModel<Emptyvia, EmptyviaWidget>("EMPTYVIA");


