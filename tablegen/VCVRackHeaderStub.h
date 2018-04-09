#include "CompanyName.hpp"
#include "util/color.hpp"
#include "dsp/digital.hpp"
#include "int64.h"
#include "Via_Macros.hpp"

// Modified light widget for the white LED

struct WhiteLight : ModuleLightWidget {
    WhiteLight() {
        addBaseColor(COLOR_WHITE);
    }
};

// Adapted light object for the glowing triangle

struct RGBTriangle : ModuleLightWidget {
    RGBTriangle() {
        addBaseColor(nvgRGBAf(1.0, 0.0, 0.0, 1.0));
        addBaseColor(nvgRGBAf(0.0, 1.0, 0.0, 1.0));
        addBaseColor(nvgRGBAf(0.0, 0.0, 1.0, 1.0));
    }
    
    void drawLight(NVGcontext *vg) {
        
        nvgBeginPath(vg);
        nvgMoveTo(vg, .4,-22.3);
        nvgLineTo(vg, -17.1,11.7);
        nvgLineTo(vg, 17.1,11.7);
        nvgClosePath(vg);
        
        
        
        // Solid color
        
        nvgFillColor(vg, color);
        nvgTransRGBAf(color, 1.0);
        nvgFill(vg);
        
        // Border
        nvgStrokeWidth(vg, 0.5);
        nvgStrokeColor(vg, borderColor);
        nvgStroke(vg);
        nvgRotate(vg, (30.0/120.0)*NVG_PI*2);
    }
    
    void drawHalo(NVGcontext *vg) {
        float radius = 14;
        float oradius = radius + 13;
        
        nvgBeginPath(vg);
        nvgRect(vg, -25, -25, 50, 50);
        
        NVGpaint paint;
        NVGcolor icol = colorMult(color, 0.10);
        NVGcolor ocol = nvgRGB(0, 0, 0);
        paint = nvgRadialGradient(vg, 0, 0, radius, oradius, icol, ocol);
        nvgFillPaint(vg, paint);
        nvgGlobalCompositeOperation(vg, NVG_LIGHTER);
        nvgFill(vg);
    }
};

// Davies knob for contrast against the black background, adapted from Rack component library
// Thanks Grayscale http://grayscale.info/ !

struct Davies1900hvia : Davies1900hKnob {
    Davies1900hvia() {
        setSVG(SVG::load(assetPlugin(plugin, "res/Davies1900hvia.svg")));
    }
};

// Button skins for the manual trigger and touch sensors

struct SH_Button : SVGSwitch, MomentarySwitch {
    SH_Button() {
        addFrame(SVG::load(assetPlugin(plugin, "res/S+H_button.svg")));
    }
};


struct Trig_Button : SVGSwitch, MomentarySwitch {
    Trig_Button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/trig_button.svg")));
    }
};


struct Freq_Button : SVGSwitch, MomentarySwitch {
    Freq_Button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/freq_button.svg")));
    }
};


struct Loop_Button : SVGSwitch, MomentarySwitch {
    Loop_Button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/loop_button.svg")));
    }
};


struct Up_Button : SVGSwitch, MomentarySwitch {
    Up_Button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/up_button.svg")));
    }
};


struct Down_Button : SVGSwitch, MomentarySwitch {
    Down_Button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/down_button.svg")));
    }
};

struct VIA_manual_button : SVGSwitch, MomentarySwitch {
    VIA_manual_button() {
        addFrame(SVG::load(assetPlugin(plugin,"res/manual_trig.svg")));
        addFrame(SVG::load(assetPlugin(plugin,"res/manual_trig_down.svg")));
    }
};

struct Via : Module {
    
    
    enum ParamIds {
        T1_PARAM,
        T2_PARAM,
        MORPH_PARAM,
        B_PARAM,
        A_PARAM,
        MORPHAMT_PARAM,
        T2AMT_PARAM,
        SH_PARAM,
        TRIG_PARAM,
        FREQ_PARAM,
        LOOP_PARAM,
        UP_PARAM,
        DOWN_PARAM,
        TRIGBUTTON_PARAM,
        NUM_PARAMS
    };
    enum InputIds {
        A_INPUT,
        B_INPUT,
        TRIG_INPUT,
        T1_INPUT,
        T2_INPUT,
        MORPH_INPUT,
        FREEZE_INPUT,
        NUM_INPUTS
    };
    enum OutputIds {
        MAIN_OUTPUT,
        LOGICA_OUTPUT,
        LOGICB_OUTPUT,
        DELTA_OUTPUT,
        NUM_OUTPUTS
    };
    enum LightIds {
        LED1_LIGHT,
        LED2_LIGHT,
        LED3_LIGHT,
        LED4_LIGHT,
        RED_LIGHT,
        GREEN_LIGHT,
        BLUE_LIGHT,
        PURPLE_LIGHT,
        NUM_LIGHTS
    };
    
    Via() : Module(NUM_PARAMS, NUM_INPUTS, NUM_OUTPUTS, NUM_LIGHTS) {}
    void step() override;
    
    SchmittTrigger trigButton;
    SchmittTrigger trigInput;
    SchmittTrigger freezeInput;
    
    struct Family {
        const uint16_t **attackFamily;
        const uint16_t **releaseFamily;
        uint32_t tableLength;
        uint32_t familySize;
        uint32_t bandlimitOff;
    };
    
    
    enum freqTypes {audio, env, seq};
    
    enum loopTypes {noloop, looping};
    
    enum trigModeTypes {noretrigger, hardsync, nongatedretrigger, gated, pendulum, pendulum2};
    
    enum sampleHoldModeTypes {nosampleandhold, a, b, ab, antidecimate, decimate};
    
    enum logicOutATypes {triggerA, gateA, deltaA};
    
    enum logicOutBTypes {triggerB, gateB, deltaB};
    
    int pressCounter;
    
    int freqMode; // {audio, env, seq}
    int loopMode; // {noloop, looping}
    int trigMode; // {noretrigger, hardsync, nongatedretrigger, gated, pendulum}
    int sampleHoldMode; // {nosampleandhold, a, b, ab, antidecimate, decimate}
    int logicOutA; // {triggerA, gateA, deltaA}
    int logicOutB;
    
    //these are the variables used to generate the phase information that feeds our interpolations
    int fixMorph;
    int getMorph;
    
    int time1;
    int time2;
    
    //most recent value from our expo decay
    int expoScale;
    
    int position;
    int holdPosition;
    int inc;
    int incSign;
    
    float attackCount;
    float releaseCount;
    int expoIndex;
    
    int out;
    
    
    bool triggerState;
    bool lastTriggerState;
    
    bool sampleA;
    bool sampleB;
    bool resampleA;
    bool resampleB;
    bool holdA;
    bool holdB;
    float aSample;
    float bSample;
    float expoCalc;
    
    int oneTime;
    
    //wavetable size - 1 in fix16 and that number doubled
    int span;
    int spanx2;
    
    //this is an integer that compensates for wavetable size in our frequency calculation (defined on wavetable family change)
    int tableSizeCompensation;
    
    //per family bit shift amounts to determine the morph  (defined on wavetable family change)
    uint32_t morphBitShiftRight;
    uint32_t morphBitShiftLeft;
    
    // helpful variable we can use for the currently selected family struct
    Family currentFamily;
    
    bool switchARTimes;
    
    int familyIndicator;
    
    uint32_t holdState;
    
    uint32_t modeFlag;
    uint32_t detectOn;
    uint32_t displayNewMode;
    
    int flagHolder;
    
    int tableHoldArray[9][517];
    
    
    void readDetect(void);
    void readRelease(uint32_t);
    void handleRelease(uint32_t);
    void changeMode(uint32_t);
    void showMode(uint32_t);
    void familyRGB(void);
    void clearLEDs(void);
    
    void loadSampleArray(Family);
    void switchFamily(void);
    
    void dacISR(void);
    void getSampleQuinticSpline(void);
    void generateDrumEnvelope(void);
    
    void (Via::*getPhase) (void);
    void getPhaseOsc(void);
    void getPhaseDrum(void);
    void getPhaseSimpleEnv(void);
    void getPhaseSimpleLFO(void);
    void getPhaseComplexEnv(void);
    void getPhaseComplexLFO(void);
    int (Via::*attackTime) (void);
    int (Via::*releaseTime) (void);
    int calcTime1Env(void);
    int calcTime2Env(void);
    int calcTime1Seq(void);
    int calcTime2Seq(void);
    
    int fix16_mul(int, int);
    int fix24_mul(int, int);
    int fix16_lerp(int, int, uint16_t);
    
    void risingEdgeHandler (void);
    void fallingEdgeHandler (void);
    void EXTI15_10_IRQHandler(void);
    void sampHoldA(void);
    void sampHoldB(void);
    
    json_t *toJson() override {
        json_t *rootJ = json_object();
        
        // freq
        json_object_set_new(rootJ, "freq", json_integer(freqMode));
        
        // loop
        json_object_set_new(rootJ, "loop", json_integer(loopMode));
        
        // trig
        json_object_set_new(rootJ, "trig", json_integer(trigMode));
        
        // SH
        json_object_set_new(rootJ, "sampleHold", json_integer(sampleHoldMode));
        
        // familyIndicator
        json_object_set_new(rootJ, "family", json_integer(familyIndicator));
        
        // flagWord
        json_object_set_new(rootJ, "flagWord", json_integer(flagHolder));
        
        // flagWord
        json_object_set_new(rootJ, "position", json_integer(position));
        
        return rootJ;
    }
    
    void fromJson(json_t *rootJ) override {
        json_t *freqJ = json_object_get(rootJ, "freq");
        freqMode = json_integer_value(freqJ);
        
        json_t *loopJ = json_object_get(rootJ, "loop");
        loopMode = json_integer_value(loopJ);
        
        json_t *trigJ = json_object_get(rootJ, "trig");
        trigMode = json_integer_value(trigJ);
        
        json_t *sampleHoldJ = json_object_get(rootJ, "sampleHold");
        sampleHoldMode = json_integer_value(sampleHoldJ);
        
        json_t *familyJ = json_object_get(rootJ, "family");
        familyIndicator = json_integer_value(familyJ);
        
        json_t *flagWordJ = json_object_get(rootJ, "flagWord");
        flagHolder = json_integer_value(flagWordJ);
        
        json_t *positionJ = json_object_get(rootJ, "position");
        position = json_integer_value(positionJ);
        
    }
    
    // wavetable definitions
    // first slopes (sample values), then groups of slopes in banks, then families as pairs of slope groups
    // declared as constant members so that they are only created once and used by all instances of the module


