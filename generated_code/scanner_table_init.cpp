#include "scanner.hpp"


void ViaScanner::fillWavetableArray(void) {

	wavetableArray[0][0] = &wavetableSet.hyperbolic_shapers;
	wavetableArray[0][1] = &wavetableSet.tanh_res;
	wavetableArray[0][2] = &wavetableSet.newBounce;
	wavetableArray[0][3] = &wavetableSet.exciteBike;
	wavetableArray[0][4] = &wavetableSet.test_fm;
	wavetableArray[0][5] = &wavetableSet.sin_phase_shift;
	wavetableArray[1][6] = &wavetableSet.bitcrush;
	wavetableArray[0][7] = &wavetableSet.new_steps;
	wavetableArray[1][0] = &wavetableSet.circular_257;
	wavetableArray[1][1] = &wavetableSet.bessel;
	wavetableArray[1][2] = &wavetableSet.additive_tri_to_pulse;
	wavetableArray[1][3] = &wavetableSet.sawBend;
	wavetableArray[1][4] = &wavetableSet.moog5Square;
	wavetableArray[1][5] = &wavetableSet.triangle_comb;
	wavetableArray[1][7] = &wavetableSet.steps5;
}

constexpr Wavetable ScannerWavetableSet::hyperbolic_shapers;
constexpr Wavetable ScannerWavetableSet::tanh_res;
constexpr Wavetable ScannerWavetableSet::newBounce;
constexpr Wavetable ScannerWavetableSet::exciteBike;
constexpr Wavetable ScannerWavetableSet::test_fm;
constexpr Wavetable ScannerWavetableSet::sin_phase_shift;
constexpr Wavetable ScannerWavetableSet::bitcrush;
constexpr Wavetable ScannerWavetableSet::new_steps;
constexpr Wavetable ScannerWavetableSet::circular_257;
constexpr Wavetable ScannerWavetableSet::bessel;
constexpr Wavetable ScannerWavetableSet::additive_tri_to_pulse;
constexpr Wavetable ScannerWavetableSet::sawBend;
constexpr Wavetable ScannerWavetableSet::moog5Square;
constexpr Wavetable ScannerWavetableSet::triangle_comb;
constexpr Wavetable ScannerWavetableSet::steps5;

constexpr const uint16_t *ScannerWavetableSet::moog5SquareShiftAttackFamily[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftAttackFamily0[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftAttackFamily1[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftAttackFamily2[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftAttackFamily3[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftAttackFamily4[];

constexpr const uint16_t *ScannerWavetableSet::moog5SquareShiftReleaseFamily[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftReleaseFamily0[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftReleaseFamily1[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftReleaseFamily2[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftReleaseFamily3[];
constexpr uint16_t ScannerWavetableSet::moog5SquareShiftReleaseFamily4[];

constexpr const uint16_t *ScannerWavetableSet::sawBendAttackFamily[];
constexpr uint16_t ScannerWavetableSet::sawBendAttackFamily0[];
constexpr uint16_t ScannerWavetableSet::sawBendAttackFamily1[];
constexpr uint16_t ScannerWavetableSet::sawBendAttackFamily2[];
constexpr uint16_t ScannerWavetableSet::sawBendAttackFamily3[];
constexpr uint16_t ScannerWavetableSet::sawBendAttackFamily4[];

constexpr const uint16_t *ScannerWavetableSet::sawBendReleaseFamily[];
constexpr uint16_t ScannerWavetableSet::sawBendReleaseFamily0[];
constexpr uint16_t ScannerWavetableSet::sawBendReleaseFamily1[];
constexpr uint16_t ScannerWavetableSet::sawBendReleaseFamily2[];
constexpr uint16_t ScannerWavetableSet::sawBendReleaseFamily3[];
constexpr uint16_t ScannerWavetableSet::sawBendReleaseFamily4[];

constexpr const uint16_t *ScannerWavetableSet::exciteBikeAttackFamily[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily0[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily1[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily2[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily3[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily4[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily5[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily6[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily7[];
constexpr uint16_t ScannerWavetableSet::exciteBikeAttackFamily8[];

constexpr const uint16_t *ScannerWavetableSet::exciteBikeReleaseFamily[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily0[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily1[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily2[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily3[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily4[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily5[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily6[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily7[];
constexpr uint16_t ScannerWavetableSet::exciteBikeReleaseFamily8[];

constexpr const uint16_t *ScannerWavetableSet::steps5AttackFamily[];
constexpr uint16_t ScannerWavetableSet::steps5AttackFamily0[];
constexpr uint16_t ScannerWavetableSet::steps5AttackFamily1[];
constexpr uint16_t ScannerWavetableSet::steps5AttackFamily2[];
constexpr uint16_t ScannerWavetableSet::steps5AttackFamily3[];
constexpr uint16_t ScannerWavetableSet::steps5AttackFamily4[];

constexpr const uint16_t *ScannerWavetableSet::steps5ReleaseFamily[];
constexpr uint16_t ScannerWavetableSet::steps5ReleaseFamily0[];
constexpr uint16_t ScannerWavetableSet::steps5ReleaseFamily1[];
constexpr uint16_t ScannerWavetableSet::steps5ReleaseFamily2[];
constexpr uint16_t ScannerWavetableSet::steps5ReleaseFamily3[];
constexpr uint16_t ScannerWavetableSet::steps5ReleaseFamily4[];

constexpr const uint16_t *ScannerWavetableSet::additive_tri_to_pulseFamily[];
constexpr uint16_t ScannerWavetableSet::additive_tri_to_pulseFamily0[];
constexpr uint16_t ScannerWavetableSet::additive_tri_to_pulseFamily1[];
constexpr uint16_t ScannerWavetableSet::additive_tri_to_pulseFamily2[];
constexpr uint16_t ScannerWavetableSet::additive_tri_to_pulseFamily3[];
constexpr uint16_t ScannerWavetableSet::additive_tri_to_pulseFamily4[];

constexpr const uint16_t *ScannerWavetableSet::newBounceFamily[];
constexpr uint16_t ScannerWavetableSet::newBounceFamily0[];
constexpr uint16_t ScannerWavetableSet::newBounceFamily1[];
constexpr uint16_t ScannerWavetableSet::newBounceFamily2[];
constexpr uint16_t ScannerWavetableSet::newBounceFamily3[];
constexpr uint16_t ScannerWavetableSet::newBounceFamily4[];

constexpr const uint16_t *ScannerWavetableSet::circular_257_slopes[];
constexpr uint16_t ScannerWavetableSet::circular_257_slopes0[];
constexpr uint16_t ScannerWavetableSet::circular_257_slopes1[];
constexpr uint16_t ScannerWavetableSet::circular_257_slopes2[];
constexpr uint16_t ScannerWavetableSet::circular_257_slopes3[];

constexpr const uint16_t *ScannerWavetableSet::test_fm_attack[];
constexpr uint16_t ScannerWavetableSet::test_fm_attack0[];
constexpr uint16_t ScannerWavetableSet::test_fm_attack1[];
constexpr uint16_t ScannerWavetableSet::test_fm_attack2[];
constexpr uint16_t ScannerWavetableSet::test_fm_attack3[];
constexpr uint16_t ScannerWavetableSet::test_fm_attack4[];

constexpr const uint16_t *ScannerWavetableSet::test_fm_release[];
constexpr uint16_t ScannerWavetableSet::test_fm_release0[];
constexpr uint16_t ScannerWavetableSet::test_fm_release1[];
constexpr uint16_t ScannerWavetableSet::test_fm_release2[];
constexpr uint16_t ScannerWavetableSet::test_fm_release3[];
constexpr uint16_t ScannerWavetableSet::test_fm_release4[];

constexpr const uint16_t *ScannerWavetableSet::triangle_comb_attack[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_attack0[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_attack1[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_attack2[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_attack3[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_attack4[];

constexpr const uint16_t *ScannerWavetableSet::triangle_comb_release[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_release0[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_release1[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_release2[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_release3[];
constexpr uint16_t ScannerWavetableSet::triangle_comb_release4[];

constexpr const uint16_t *ScannerWavetableSet::tanh_res_attack[];
constexpr uint16_t ScannerWavetableSet::tanh_res_attack0[];
constexpr uint16_t ScannerWavetableSet::tanh_res_attack1[];
constexpr uint16_t ScannerWavetableSet::tanh_res_attack2[];
constexpr uint16_t ScannerWavetableSet::tanh_res_attack3[];
constexpr uint16_t ScannerWavetableSet::tanh_res_attack4[];

constexpr const uint16_t *ScannerWavetableSet::tanh_res_release[];
constexpr uint16_t ScannerWavetableSet::tanh_res_release0[];
constexpr uint16_t ScannerWavetableSet::tanh_res_release1[];
constexpr uint16_t ScannerWavetableSet::tanh_res_release2[];
constexpr uint16_t ScannerWavetableSet::tanh_res_release3[];
constexpr uint16_t ScannerWavetableSet::tanh_res_release4[];

constexpr const uint16_t *ScannerWavetableSet::hyperbolic_shapers_attack[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_attack0[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_attack1[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_attack2[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_attack3[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_attack4[];

constexpr const uint16_t *ScannerWavetableSet::hyperbolic_shapers_release[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_release0[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_release1[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_release2[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_release3[];
constexpr uint16_t ScannerWavetableSet::hyperbolic_shapers_release4[];

constexpr const uint16_t *ScannerWavetableSet::bitcrush_attack[];
constexpr uint16_t ScannerWavetableSet::bitcrush_attack0[];
constexpr uint16_t ScannerWavetableSet::bitcrush_attack1[];
constexpr uint16_t ScannerWavetableSet::bitcrush_attack2[];
constexpr uint16_t ScannerWavetableSet::bitcrush_attack3[];
constexpr uint16_t ScannerWavetableSet::bitcrush_attack4[];

constexpr const uint16_t *ScannerWavetableSet::bitcrush_release[];
constexpr uint16_t ScannerWavetableSet::bitcrush_release0[];
constexpr uint16_t ScannerWavetableSet::bitcrush_release1[];
constexpr uint16_t ScannerWavetableSet::bitcrush_release2[];
constexpr uint16_t ScannerWavetableSet::bitcrush_release3[];
constexpr uint16_t ScannerWavetableSet::bitcrush_release4[];

constexpr const uint16_t *ScannerWavetableSet::new_steps_attack[];
constexpr uint16_t ScannerWavetableSet::new_steps_attack0[];
constexpr uint16_t ScannerWavetableSet::new_steps_attack1[];
constexpr uint16_t ScannerWavetableSet::new_steps_attack2[];
constexpr uint16_t ScannerWavetableSet::new_steps_attack3[];
constexpr uint16_t ScannerWavetableSet::new_steps_attack4[];

constexpr const uint16_t *ScannerWavetableSet::new_steps_release[];
constexpr uint16_t ScannerWavetableSet::new_steps_release0[];
constexpr uint16_t ScannerWavetableSet::new_steps_release1[];
constexpr uint16_t ScannerWavetableSet::new_steps_release2[];
constexpr uint16_t ScannerWavetableSet::new_steps_release3[];
constexpr uint16_t ScannerWavetableSet::new_steps_release4[];

constexpr const uint16_t *ScannerWavetableSet::bessel_attack[];
constexpr uint16_t ScannerWavetableSet::bessel_attack0[];
constexpr uint16_t ScannerWavetableSet::bessel_attack1[];
constexpr uint16_t ScannerWavetableSet::bessel_attack2[];
constexpr uint16_t ScannerWavetableSet::bessel_attack3[];
constexpr uint16_t ScannerWavetableSet::bessel_attack4[];

constexpr const uint16_t *ScannerWavetableSet::bessel_release[];
constexpr uint16_t ScannerWavetableSet::bessel_release0[];
constexpr uint16_t ScannerWavetableSet::bessel_release1[];
constexpr uint16_t ScannerWavetableSet::bessel_release2[];
constexpr uint16_t ScannerWavetableSet::bessel_release3[];
constexpr uint16_t ScannerWavetableSet::bessel_release4[];

constexpr const uint16_t *ScannerWavetableSet::sin_phase_shift_attack[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_attack0[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_attack1[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_attack2[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_attack3[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_attack4[];

constexpr const uint16_t *ScannerWavetableSet::sin_phase_shift_release[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_release0[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_release1[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_release2[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_release3[];
constexpr uint16_t ScannerWavetableSet::sin_phase_shift_release4[];


// declare functions to set the currently active tables
void ViaScanner::switchWavetableX(const Wavetable * table) {
	wavetableSet.loadWavetableWithDiff15BitSlope(table, (uint32_t *) wavetableXRead);
	scanner.xTableSize = table->numWaveforms - 1;
}

// declare functions to set the currently active tables
void ViaScanner::switchWavetableY(const Wavetable * table) {
	wavetableSet.loadWavetableWithDiff15BitSlope(table, (uint32_t *) wavetableYRead);
	scanner.yTableSize = table->numWaveforms - 1;
}