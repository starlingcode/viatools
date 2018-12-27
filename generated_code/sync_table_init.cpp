#include "sync.hpp"


void ViaSync::fillWavetableArray(void) {

	wavetableArray[	0][0] = &wavetableSet.ascendingAdditiveClamp;
	wavetableArray[	0][1] = &wavetableSet.linwavefold_257;
	wavetableArray[	0][2] = &wavetableSet.newBounce;
	wavetableArray[	0][3] = &wavetableSet.circular_257;
	wavetableArray[	1][0] = &wavetableSet.impevens;
	wavetableArray[	1][1] = &wavetableSet.additive_tri_to_pulse;
	wavetableArray[	1][2] = &wavetableSet.perlin;
	wavetableArray[	1][3] = &wavetableSet.csound_formants;
	wavetableArray[	2][0] = &wavetableSet.additive_pairs;
	wavetableArray[	2][1] = &wavetableSet.moogSquare;
	wavetableArray[	2][2] = &wavetableSet.test_fm;
	wavetableArray[	2][3] = &wavetableSet.trains;
	wavetableArray[	3][0] = &wavetableSet.sharpExpoSym;
	wavetableArray[	3][1] = &wavetableSet.gammaAsym;
	wavetableArray[	3][2] = &wavetableSet.newest_steps;
	wavetableArray[	3][3] = &wavetableSet.block_test;
	wavetableArrayGlobal[0] = &wavetableSet.triOdd;
	wavetableArrayGlobal[1] = &wavetableSet.sinwavefold_257;
	wavetableArrayGlobal[2] = &wavetableSet.euclidean_test;
	wavetableArrayGlobal[3] = &wavetableSet.skipSaw;
}

constexpr Wavetable SyncWavetableSet::ascendingAdditiveClamp;
constexpr Wavetable SyncWavetableSet::linwavefold_257;
constexpr Wavetable SyncWavetableSet::newBounce;
constexpr Wavetable SyncWavetableSet::circular_257;
constexpr Wavetable SyncWavetableSet::impevens;
constexpr Wavetable SyncWavetableSet::additive_tri_to_pulse;
constexpr Wavetable SyncWavetableSet::perlin;
constexpr Wavetable SyncWavetableSet::csound_formants;
constexpr Wavetable SyncWavetableSet::additive_pairs;
constexpr Wavetable SyncWavetableSet::moogSquare;
constexpr Wavetable SyncWavetableSet::test_fm;
constexpr Wavetable SyncWavetableSet::trains;
constexpr Wavetable SyncWavetableSet::sharpExpoSym;
constexpr Wavetable SyncWavetableSet::gammaAsym;
constexpr Wavetable SyncWavetableSet::newest_steps;
constexpr Wavetable SyncWavetableSet::block_test;
constexpr Wavetable SyncWavetableSet::triOdd;
constexpr Wavetable SyncWavetableSet::sinwavefold_257;
constexpr Wavetable SyncWavetableSet::euclidean_test;
constexpr Wavetable SyncWavetableSet::skipSaw;

constexpr const uint16_t *SyncWavetableSet::moogSquareShiftAttackFamily[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily0[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily1[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily2[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily3[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily4[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily5[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily6[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily7[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::moogSquareShiftReleaseFamily[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::moogSquareShiftReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::perlinAttackFamily[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily0[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily1[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily2[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily3[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily4[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily5[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily6[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily7[];
constexpr uint16_t SyncWavetableSet::perlinAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::perlinReleaseFamily[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::perlinReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::trioddAttackFamily[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily0[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily1[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily2[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily3[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily4[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily5[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily6[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily7[];
constexpr uint16_t SyncWavetableSet::trioddAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::trioddReleaseFamily[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::trioddReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::gammaAsymAttackFamily[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily0[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily1[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily2[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily3[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily4[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily5[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily6[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily7[];
constexpr uint16_t SyncWavetableSet::gammaAsymAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::gammaAsymReleaseFamily[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::gammaAsymReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::sharpExpoSymAttackFamily[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily0[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily1[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily2[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily3[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily4[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily5[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily6[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily7[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::sharpExpoSymReleaseFamily[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::sharpExpoSymReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::ascendingAdditiveClampAttackFamily[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily0[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily1[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily2[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily3[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily4[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily5[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily6[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily7[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampAttackFamily8[];

constexpr const uint16_t *SyncWavetableSet::ascendingAdditiveClampReleaseFamily[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily0[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily1[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily2[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily3[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily4[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily5[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily6[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily7[];
constexpr uint16_t SyncWavetableSet::ascendingAdditiveClampReleaseFamily8[];

constexpr const uint16_t *SyncWavetableSet::impshort[];
constexpr uint16_t SyncWavetableSet::impshort0[];
constexpr uint16_t SyncWavetableSet::impshort1[];
constexpr uint16_t SyncWavetableSet::impshort2[];
constexpr uint16_t SyncWavetableSet::impshort3[];
constexpr uint16_t SyncWavetableSet::impshort4[];
constexpr uint16_t SyncWavetableSet::impshort5[];
constexpr uint16_t SyncWavetableSet::impshort6[];
constexpr uint16_t SyncWavetableSet::impshort7[];
constexpr uint16_t SyncWavetableSet::impshort8[];

constexpr const uint16_t *SyncWavetableSet::skipsaw[];
constexpr uint16_t SyncWavetableSet::skipsaw0[];
constexpr uint16_t SyncWavetableSet::skipsaw1[];
constexpr uint16_t SyncWavetableSet::skipsaw2[];
constexpr uint16_t SyncWavetableSet::skipsaw3[];
constexpr uint16_t SyncWavetableSet::skipsaw4[];

constexpr const uint16_t *SyncWavetableSet::linwavefold_257_Family[];
constexpr uint16_t SyncWavetableSet::linwavefold_257_Family0[];
constexpr uint16_t SyncWavetableSet::linwavefold_257_Family1[];
constexpr uint16_t SyncWavetableSet::linwavefold_257_Family2[];
constexpr uint16_t SyncWavetableSet::linwavefold_257_Family3[];
constexpr uint16_t SyncWavetableSet::linwavefold_257_Family4[];

constexpr const uint16_t *SyncWavetableSet::sinwavefold_257_Family[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family0[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family1[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family2[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family3[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family4[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family5[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family6[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family7[];
constexpr uint16_t SyncWavetableSet::sinwavefold_257_Family8[];

constexpr const uint16_t *SyncWavetableSet::additive_tri_to_pulseFamily[];
constexpr uint16_t SyncWavetableSet::additive_tri_to_pulseFamily0[];
constexpr uint16_t SyncWavetableSet::additive_tri_to_pulseFamily1[];
constexpr uint16_t SyncWavetableSet::additive_tri_to_pulseFamily2[];
constexpr uint16_t SyncWavetableSet::additive_tri_to_pulseFamily3[];
constexpr uint16_t SyncWavetableSet::additive_tri_to_pulseFamily4[];

constexpr const uint16_t *SyncWavetableSet::newBounceFamily[];
constexpr uint16_t SyncWavetableSet::newBounceFamily0[];
constexpr uint16_t SyncWavetableSet::newBounceFamily1[];
constexpr uint16_t SyncWavetableSet::newBounceFamily2[];
constexpr uint16_t SyncWavetableSet::newBounceFamily3[];
constexpr uint16_t SyncWavetableSet::newBounceFamily4[];

constexpr const uint16_t *SyncWavetableSet::circular_257_slopes[];
constexpr uint16_t SyncWavetableSet::circular_257_slopes0[];
constexpr uint16_t SyncWavetableSet::circular_257_slopes1[];
constexpr uint16_t SyncWavetableSet::circular_257_slopes2[];
constexpr uint16_t SyncWavetableSet::circular_257_slopes3[];

constexpr const uint16_t *SyncWavetableSet::test_fm_attack[];
constexpr uint16_t SyncWavetableSet::test_fm_attack0[];
constexpr uint16_t SyncWavetableSet::test_fm_attack1[];
constexpr uint16_t SyncWavetableSet::test_fm_attack2[];
constexpr uint16_t SyncWavetableSet::test_fm_attack3[];
constexpr uint16_t SyncWavetableSet::test_fm_attack4[];

constexpr const uint16_t *SyncWavetableSet::test_fm_release[];
constexpr uint16_t SyncWavetableSet::test_fm_release0[];
constexpr uint16_t SyncWavetableSet::test_fm_release1[];
constexpr uint16_t SyncWavetableSet::test_fm_release2[];
constexpr uint16_t SyncWavetableSet::test_fm_release3[];
constexpr uint16_t SyncWavetableSet::test_fm_release4[];

constexpr const uint16_t *SyncWavetableSet::trains_attack[];
constexpr uint16_t SyncWavetableSet::trains_attack0[];
constexpr uint16_t SyncWavetableSet::trains_attack1[];
constexpr uint16_t SyncWavetableSet::trains_attack2[];
constexpr uint16_t SyncWavetableSet::trains_attack3[];
constexpr uint16_t SyncWavetableSet::trains_attack4[];
constexpr uint16_t SyncWavetableSet::trains_attack5[];
constexpr uint16_t SyncWavetableSet::trains_attack6[];
constexpr uint16_t SyncWavetableSet::trains_attack7[];
constexpr uint16_t SyncWavetableSet::trains_attack8[];

constexpr const uint16_t *SyncWavetableSet::trains_release[];
constexpr uint16_t SyncWavetableSet::trains_release0[];
constexpr uint16_t SyncWavetableSet::trains_release1[];
constexpr uint16_t SyncWavetableSet::trains_release2[];
constexpr uint16_t SyncWavetableSet::trains_release3[];
constexpr uint16_t SyncWavetableSet::trains_release4[];
constexpr uint16_t SyncWavetableSet::trains_release5[];
constexpr uint16_t SyncWavetableSet::trains_release6[];
constexpr uint16_t SyncWavetableSet::trains_release7[];
constexpr uint16_t SyncWavetableSet::trains_release8[];

constexpr const uint16_t *SyncWavetableSet::csound_formants_attack[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack0[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack1[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack2[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack3[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack4[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack5[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack6[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack7[];
constexpr uint16_t SyncWavetableSet::csound_formants_attack8[];

constexpr const uint16_t *SyncWavetableSet::csound_formants_release[];
constexpr uint16_t SyncWavetableSet::csound_formants_release0[];
constexpr uint16_t SyncWavetableSet::csound_formants_release1[];
constexpr uint16_t SyncWavetableSet::csound_formants_release2[];
constexpr uint16_t SyncWavetableSet::csound_formants_release3[];
constexpr uint16_t SyncWavetableSet::csound_formants_release4[];
constexpr uint16_t SyncWavetableSet::csound_formants_release5[];
constexpr uint16_t SyncWavetableSet::csound_formants_release6[];
constexpr uint16_t SyncWavetableSet::csound_formants_release7[];
constexpr uint16_t SyncWavetableSet::csound_formants_release8[];

constexpr const uint16_t *SyncWavetableSet::additive_pairs_slopes[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes0[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes1[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes2[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes3[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes4[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes5[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes6[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes7[];
constexpr uint16_t SyncWavetableSet::additive_pairs_slopes8[];

constexpr const uint16_t *SyncWavetableSet::euclidean_test_slopes[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes0[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes1[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes2[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes3[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes4[];
constexpr uint16_t SyncWavetableSet::euclidean_test_slopes5[];

constexpr const uint16_t *SyncWavetableSet::block_test_attack[];
constexpr uint16_t SyncWavetableSet::block_test_attack0[];
constexpr uint16_t SyncWavetableSet::block_test_attack1[];
constexpr uint16_t SyncWavetableSet::block_test_attack2[];
constexpr uint16_t SyncWavetableSet::block_test_attack3[];
constexpr uint16_t SyncWavetableSet::block_test_attack4[];
constexpr uint16_t SyncWavetableSet::block_test_attack5[];
constexpr uint16_t SyncWavetableSet::block_test_attack6[];
constexpr uint16_t SyncWavetableSet::block_test_attack7[];
constexpr uint16_t SyncWavetableSet::block_test_attack8[];

constexpr const uint16_t *SyncWavetableSet::block_test_release[];
constexpr uint16_t SyncWavetableSet::block_test_release0[];
constexpr uint16_t SyncWavetableSet::block_test_release1[];
constexpr uint16_t SyncWavetableSet::block_test_release2[];
constexpr uint16_t SyncWavetableSet::block_test_release3[];
constexpr uint16_t SyncWavetableSet::block_test_release4[];
constexpr uint16_t SyncWavetableSet::block_test_release5[];
constexpr uint16_t SyncWavetableSet::block_test_release6[];
constexpr uint16_t SyncWavetableSet::block_test_release7[];
constexpr uint16_t SyncWavetableSet::block_test_release8[];

constexpr const uint16_t *SyncWavetableSet::newest_steps_attack[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack0[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack1[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack2[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack3[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack4[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack5[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack6[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack7[];
constexpr uint16_t SyncWavetableSet::newest_steps_attack8[];

constexpr const uint16_t *SyncWavetableSet::newest_steps_release[];
constexpr uint16_t SyncWavetableSet::newest_steps_release0[];
constexpr uint16_t SyncWavetableSet::newest_steps_release1[];
constexpr uint16_t SyncWavetableSet::newest_steps_release2[];
constexpr uint16_t SyncWavetableSet::newest_steps_release3[];
constexpr uint16_t SyncWavetableSet::newest_steps_release4[];
constexpr uint16_t SyncWavetableSet::newest_steps_release5[];
constexpr uint16_t SyncWavetableSet::newest_steps_release6[];
constexpr uint16_t SyncWavetableSet::newest_steps_release7[];
constexpr uint16_t SyncWavetableSet::newest_steps_release8[];


// declare functions to set the currently active tables
void ViaSync::switchWavetable(const Wavetable * table) {
	wavetableSet.loadWavetableWithDiff(table, (uint32_t *) wavetableRead);
	syncWavetable.tableSize = table->numWaveforms - 1;
}

// declare functions to set the currently active tables
void ViaSync::switchWavetableGlobal(const Wavetable * table) {
	wavetableSet.loadWavetableWithDiff(table, (uint32_t *) wavetableRead);
	syncWavetable.tableSize = table->numWaveforms - 1;
}

//// declare functions to set the currently active tables
//void ViaSync::initPhaseDistTable(void) {
//	loadPhaseDistTable(&phaseDistPWM, phaseDistRead);
//}

