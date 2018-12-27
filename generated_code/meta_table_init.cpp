#include "meta.hpp"


void ViaMeta::fillWavetableArray(void) {

	wavetableArray[0][0] = &wavetableSet.impevens;
	wavetableArray[0][1] = &wavetableSet.additive_pairs;
	wavetableArray[0][2] = &wavetableSet.linwavefold_257;
	wavetableArray[2][0] = &wavetableSet.skipSaw;
	wavetableArray[0][4] = &wavetableSet.csound_formants;
	wavetableArray[0][5] = &wavetableSet.perlin;
	wavetableArray[0][6] = &wavetableSet.trains;
	wavetableArray[0][7] = &wavetableSet.vox;
	wavetableArray[1][0] = &wavetableSet.gammaAsym;
	wavetableArray[1][1] = &wavetableSet.sharpLinSym;
	wavetableArray[1][2] = &wavetableSet.circular_257;
	wavetableArray[1][3] = &wavetableSet.quintic_outinAsym;
	wavetableArray[1][4] = &wavetableSet.doubleLump3rdDegLinAtk;
	wavetableArray[1][5] = &wavetableSet.lump2ndDegLinAtk;
	wavetableArray[1][6] = &wavetableSet.testRMS2;
	wavetableArray[1][7] = &wavetableSet.testRMS;
	wavetableArray[2][1] = &wavetableSet.euclidean_test;
	wavetableArray[2][2] = &wavetableSet.bounce;
	wavetableArray[2][3] = &wavetableSet.bounce_257;
	wavetableArray[2][4] = &wavetableSet.sawBend;
	wavetableArray[2][5] = &wavetableSet.exciteBike;
	wavetableArray[2][6] = &wavetableSet.newest_steps;
	wavetableArray[2][7] = &wavetableSet.block_test;
}

constexpr Wavetable MetaWavetableSet::impevens;
constexpr Wavetable MetaWavetableSet::additive_pairs;
constexpr Wavetable MetaWavetableSet::linwavefold_257;
constexpr Wavetable MetaWavetableSet::skipSaw;
constexpr Wavetable MetaWavetableSet::csound_formants;
constexpr Wavetable MetaWavetableSet::perlin;
constexpr Wavetable MetaWavetableSet::trains;
constexpr Wavetable MetaWavetableSet::vox;
constexpr Wavetable MetaWavetableSet::gammaAsym;
constexpr Wavetable MetaWavetableSet::sharpLinSym;
constexpr Wavetable MetaWavetableSet::circular_257;
constexpr Wavetable MetaWavetableSet::quintic_outinAsym;
constexpr Wavetable MetaWavetableSet::doubleLump3rdDegLinAtk;
constexpr Wavetable MetaWavetableSet::lump2ndDegLinAtk;
constexpr Wavetable MetaWavetableSet::testRMS2;
constexpr Wavetable MetaWavetableSet::testRMS;
constexpr Wavetable MetaWavetableSet::euclidean_test;
constexpr Wavetable MetaWavetableSet::bounce;
constexpr Wavetable MetaWavetableSet::bounce_257;
constexpr Wavetable MetaWavetableSet::sawBend;
constexpr Wavetable MetaWavetableSet::exciteBike;
constexpr Wavetable MetaWavetableSet::newest_steps;
constexpr Wavetable MetaWavetableSet::block_test;

constexpr const uint16_t *MetaWavetableSet::perlinAttackFamily[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily0[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily1[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily2[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily3[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily4[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily5[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily6[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily7[];
constexpr uint16_t MetaWavetableSet::perlinAttackFamily8[];

constexpr const uint16_t *MetaWavetableSet::perlinReleaseFamily[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily4[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily5[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily6[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily7[];
constexpr uint16_t MetaWavetableSet::perlinReleaseFamily8[];

constexpr const uint16_t *MetaWavetableSet::bounceAttackFamily[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily0[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily1[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily2[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily3[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily4[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily5[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily6[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily7[];
constexpr uint16_t MetaWavetableSet::bounceAttackFamily8[];

constexpr const uint16_t *MetaWavetableSet::bounceReleaseFamily[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily4[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily5[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily6[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily7[];
constexpr uint16_t MetaWavetableSet::bounceReleaseFamily8[];

constexpr const uint16_t *MetaWavetableSet::sawBendAttackFamily[];
constexpr uint16_t MetaWavetableSet::sawBendAttackFamily0[];
constexpr uint16_t MetaWavetableSet::sawBendAttackFamily1[];
constexpr uint16_t MetaWavetableSet::sawBendAttackFamily2[];
constexpr uint16_t MetaWavetableSet::sawBendAttackFamily3[];
constexpr uint16_t MetaWavetableSet::sawBendAttackFamily4[];

constexpr const uint16_t *MetaWavetableSet::sawBendReleaseFamily[];
constexpr uint16_t MetaWavetableSet::sawBendReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::sawBendReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::sawBendReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::sawBendReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::sawBendReleaseFamily4[];

constexpr const uint16_t *MetaWavetableSet::exciteBikeAttackFamily[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily0[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily1[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily2[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily3[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily4[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily5[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily6[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily7[];
constexpr uint16_t MetaWavetableSet::exciteBikeAttackFamily8[];

constexpr const uint16_t *MetaWavetableSet::exciteBikeReleaseFamily[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily4[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily5[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily6[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily7[];
constexpr uint16_t MetaWavetableSet::exciteBikeReleaseFamily8[];

constexpr const uint16_t *MetaWavetableSet::gammaAsymAttackFamily[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily0[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily1[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily2[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily3[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily4[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily5[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily6[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily7[];
constexpr uint16_t MetaWavetableSet::gammaAsymAttackFamily8[];

constexpr const uint16_t *MetaWavetableSet::gammaAsymReleaseFamily[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily4[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily5[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily6[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily7[];
constexpr uint16_t MetaWavetableSet::gammaAsymReleaseFamily8[];

constexpr const uint16_t *MetaWavetableSet::sharpLinSymAttackFamily[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily0[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily1[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily2[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily3[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily4[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily5[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily6[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily7[];
constexpr uint16_t MetaWavetableSet::sharpLinSymAttackFamily8[];

constexpr const uint16_t *MetaWavetableSet::sharpLinSymReleaseFamily[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily0[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily1[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily2[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily3[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily4[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily5[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily6[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily7[];
constexpr uint16_t MetaWavetableSet::sharpLinSymReleaseFamily8[];

constexpr const uint16_t *MetaWavetableSet::impshort[];
constexpr uint16_t MetaWavetableSet::impshort0[];
constexpr uint16_t MetaWavetableSet::impshort1[];
constexpr uint16_t MetaWavetableSet::impshort2[];
constexpr uint16_t MetaWavetableSet::impshort3[];
constexpr uint16_t MetaWavetableSet::impshort4[];
constexpr uint16_t MetaWavetableSet::impshort5[];
constexpr uint16_t MetaWavetableSet::impshort6[];
constexpr uint16_t MetaWavetableSet::impshort7[];
constexpr uint16_t MetaWavetableSet::impshort8[];

constexpr const uint16_t *MetaWavetableSet::skipsaw[];
constexpr uint16_t MetaWavetableSet::skipsaw0[];
constexpr uint16_t MetaWavetableSet::skipsaw1[];
constexpr uint16_t MetaWavetableSet::skipsaw2[];
constexpr uint16_t MetaWavetableSet::skipsaw3[];
constexpr uint16_t MetaWavetableSet::skipsaw4[];

constexpr const uint16_t *MetaWavetableSet::allLinear129_5[];
constexpr uint16_t MetaWavetableSet::allLinear129_50[];
constexpr uint16_t MetaWavetableSet::allLinear129_51[];
constexpr uint16_t MetaWavetableSet::allLinear129_52[];
constexpr uint16_t MetaWavetableSet::allLinear129_53[];
constexpr uint16_t MetaWavetableSet::allLinear129_54[];

constexpr const uint16_t *MetaWavetableSet::lump2ndDeg[];
constexpr uint16_t MetaWavetableSet::lump2ndDeg0[];
constexpr uint16_t MetaWavetableSet::lump2ndDeg1[];
constexpr uint16_t MetaWavetableSet::lump2ndDeg2[];
constexpr uint16_t MetaWavetableSet::lump2ndDeg3[];
constexpr uint16_t MetaWavetableSet::lump2ndDeg4[];

constexpr const uint16_t *MetaWavetableSet::lump3rdDeg[];
constexpr uint16_t MetaWavetableSet::lump3rdDeg0[];
constexpr uint16_t MetaWavetableSet::lump3rdDeg1[];
constexpr uint16_t MetaWavetableSet::lump3rdDeg2[];
constexpr uint16_t MetaWavetableSet::lump3rdDeg3[];
constexpr uint16_t MetaWavetableSet::lump3rdDeg4[];

constexpr const uint16_t *MetaWavetableSet::linwavefold_257_Family[];
constexpr uint16_t MetaWavetableSet::linwavefold_257_Family0[];
constexpr uint16_t MetaWavetableSet::linwavefold_257_Family1[];
constexpr uint16_t MetaWavetableSet::linwavefold_257_Family2[];
constexpr uint16_t MetaWavetableSet::linwavefold_257_Family3[];
constexpr uint16_t MetaWavetableSet::linwavefold_257_Family4[];

constexpr const uint16_t *MetaWavetableSet::testRMS_release[];
constexpr uint16_t MetaWavetableSet::testRMS_release0[];
constexpr uint16_t MetaWavetableSet::testRMS_release1[];
constexpr uint16_t MetaWavetableSet::testRMS_release2[];
constexpr uint16_t MetaWavetableSet::testRMS_release3[];
constexpr uint16_t MetaWavetableSet::testRMS_release4[];

constexpr const uint16_t *MetaWavetableSet::bounce_257_slopes[];
constexpr uint16_t MetaWavetableSet::bounce_257_slopes0[];
constexpr uint16_t MetaWavetableSet::bounce_257_slopes1[];
constexpr uint16_t MetaWavetableSet::bounce_257_slopes2[];
constexpr uint16_t MetaWavetableSet::bounce_257_slopes3[];
constexpr uint16_t MetaWavetableSet::bounce_257_slopes4[];

constexpr const uint16_t *MetaWavetableSet::circular_257_slopes[];
constexpr uint16_t MetaWavetableSet::circular_257_slopes0[];
constexpr uint16_t MetaWavetableSet::circular_257_slopes1[];
constexpr uint16_t MetaWavetableSet::circular_257_slopes2[];
constexpr uint16_t MetaWavetableSet::circular_257_slopes3[];

constexpr const uint16_t *MetaWavetableSet::quintic_outin2quintic_inout257_slopes[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes0[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes1[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes2[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes3[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes4[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes5[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes6[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes7[];
constexpr uint16_t MetaWavetableSet::quintic_outin2quintic_inout257_slopes8[];

constexpr const uint16_t *MetaWavetableSet::quintic_inout2quintic_outin257_slopes[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes0[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes1[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes2[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes3[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes4[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes5[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes6[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes7[];
constexpr uint16_t MetaWavetableSet::quintic_inout2quintic_outin257_slopes8[];

constexpr const uint16_t *MetaWavetableSet::trains_attack[];
constexpr uint16_t MetaWavetableSet::trains_attack0[];
constexpr uint16_t MetaWavetableSet::trains_attack1[];
constexpr uint16_t MetaWavetableSet::trains_attack2[];
constexpr uint16_t MetaWavetableSet::trains_attack3[];
constexpr uint16_t MetaWavetableSet::trains_attack4[];
constexpr uint16_t MetaWavetableSet::trains_attack5[];
constexpr uint16_t MetaWavetableSet::trains_attack6[];
constexpr uint16_t MetaWavetableSet::trains_attack7[];
constexpr uint16_t MetaWavetableSet::trains_attack8[];

constexpr const uint16_t *MetaWavetableSet::trains_release[];
constexpr uint16_t MetaWavetableSet::trains_release0[];
constexpr uint16_t MetaWavetableSet::trains_release1[];
constexpr uint16_t MetaWavetableSet::trains_release2[];
constexpr uint16_t MetaWavetableSet::trains_release3[];
constexpr uint16_t MetaWavetableSet::trains_release4[];
constexpr uint16_t MetaWavetableSet::trains_release5[];
constexpr uint16_t MetaWavetableSet::trains_release6[];
constexpr uint16_t MetaWavetableSet::trains_release7[];
constexpr uint16_t MetaWavetableSet::trains_release8[];

constexpr const uint16_t *MetaWavetableSet::vox_attack[];
constexpr uint16_t MetaWavetableSet::vox_attack0[];
constexpr uint16_t MetaWavetableSet::vox_attack1[];
constexpr uint16_t MetaWavetableSet::vox_attack2[];
constexpr uint16_t MetaWavetableSet::vox_attack3[];
constexpr uint16_t MetaWavetableSet::vox_attack4[];
constexpr uint16_t MetaWavetableSet::vox_attack5[];
constexpr uint16_t MetaWavetableSet::vox_attack6[];
constexpr uint16_t MetaWavetableSet::vox_attack7[];
constexpr uint16_t MetaWavetableSet::vox_attack8[];

constexpr const uint16_t *MetaWavetableSet::vox_release[];
constexpr uint16_t MetaWavetableSet::vox_release0[];
constexpr uint16_t MetaWavetableSet::vox_release1[];
constexpr uint16_t MetaWavetableSet::vox_release2[];
constexpr uint16_t MetaWavetableSet::vox_release3[];
constexpr uint16_t MetaWavetableSet::vox_release4[];
constexpr uint16_t MetaWavetableSet::vox_release5[];
constexpr uint16_t MetaWavetableSet::vox_release6[];
constexpr uint16_t MetaWavetableSet::vox_release7[];
constexpr uint16_t MetaWavetableSet::vox_release8[];

constexpr const uint16_t *MetaWavetableSet::csound_formants_attack[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack0[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack1[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack2[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack3[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack4[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack5[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack6[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack7[];
constexpr uint16_t MetaWavetableSet::csound_formants_attack8[];

constexpr const uint16_t *MetaWavetableSet::csound_formants_release[];
constexpr uint16_t MetaWavetableSet::csound_formants_release0[];
constexpr uint16_t MetaWavetableSet::csound_formants_release1[];
constexpr uint16_t MetaWavetableSet::csound_formants_release2[];
constexpr uint16_t MetaWavetableSet::csound_formants_release3[];
constexpr uint16_t MetaWavetableSet::csound_formants_release4[];
constexpr uint16_t MetaWavetableSet::csound_formants_release5[];
constexpr uint16_t MetaWavetableSet::csound_formants_release6[];
constexpr uint16_t MetaWavetableSet::csound_formants_release7[];
constexpr uint16_t MetaWavetableSet::csound_formants_release8[];

constexpr const uint16_t *MetaWavetableSet::additive_pairs_slopes[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes0[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes1[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes2[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes3[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes4[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes5[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes6[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes7[];
constexpr uint16_t MetaWavetableSet::additive_pairs_slopes8[];

constexpr const uint16_t *MetaWavetableSet::testRMS2_release[];
constexpr uint16_t MetaWavetableSet::testRMS2_release0[];
constexpr uint16_t MetaWavetableSet::testRMS2_release1[];
constexpr uint16_t MetaWavetableSet::testRMS2_release2[];
constexpr uint16_t MetaWavetableSet::testRMS2_release3[];
constexpr uint16_t MetaWavetableSet::testRMS2_release4[];

constexpr const uint16_t *MetaWavetableSet::euclidean_test_slopes[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes0[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes1[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes2[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes3[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes4[];
constexpr uint16_t MetaWavetableSet::euclidean_test_slopes5[];

constexpr const uint16_t *MetaWavetableSet::block_test_attack[];
constexpr uint16_t MetaWavetableSet::block_test_attack0[];
constexpr uint16_t MetaWavetableSet::block_test_attack1[];
constexpr uint16_t MetaWavetableSet::block_test_attack2[];
constexpr uint16_t MetaWavetableSet::block_test_attack3[];
constexpr uint16_t MetaWavetableSet::block_test_attack4[];
constexpr uint16_t MetaWavetableSet::block_test_attack5[];
constexpr uint16_t MetaWavetableSet::block_test_attack6[];
constexpr uint16_t MetaWavetableSet::block_test_attack7[];
constexpr uint16_t MetaWavetableSet::block_test_attack8[];

constexpr const uint16_t *MetaWavetableSet::block_test_release[];
constexpr uint16_t MetaWavetableSet::block_test_release0[];
constexpr uint16_t MetaWavetableSet::block_test_release1[];
constexpr uint16_t MetaWavetableSet::block_test_release2[];
constexpr uint16_t MetaWavetableSet::block_test_release3[];
constexpr uint16_t MetaWavetableSet::block_test_release4[];
constexpr uint16_t MetaWavetableSet::block_test_release5[];
constexpr uint16_t MetaWavetableSet::block_test_release6[];
constexpr uint16_t MetaWavetableSet::block_test_release7[];
constexpr uint16_t MetaWavetableSet::block_test_release8[];

constexpr const uint16_t *MetaWavetableSet::newest_steps_attack[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack0[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack1[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack2[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack3[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack4[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack5[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack6[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack7[];
constexpr uint16_t MetaWavetableSet::newest_steps_attack8[];

constexpr const uint16_t *MetaWavetableSet::newest_steps_release[];
constexpr uint16_t MetaWavetableSet::newest_steps_release0[];
constexpr uint16_t MetaWavetableSet::newest_steps_release1[];
constexpr uint16_t MetaWavetableSet::newest_steps_release2[];
constexpr uint16_t MetaWavetableSet::newest_steps_release3[];
constexpr uint16_t MetaWavetableSet::newest_steps_release4[];
constexpr uint16_t MetaWavetableSet::newest_steps_release5[];
constexpr uint16_t MetaWavetableSet::newest_steps_release6[];
constexpr uint16_t MetaWavetableSet::newest_steps_release7[];
constexpr uint16_t MetaWavetableSet::newest_steps_release8[];


// declare functions to set the currently active tables
void ViaMeta::switchWavetable(const Wavetable * table) {
	wavetableSet.loadWavetableWithDiff15Bit(table, (uint32_t *) wavetableRead);
	metaWavetable.tableSize = table->numWaveforms - 1;
}

// declare functions to set the currently active tables
void ViaMeta::initDrum(void) {
	wavetableSet.loadSingleTable15Bit(&wavetableSet.drum, (uint32_t *) wavetableReadDrum);
	for (int32_t i = 0; i < 4; i++) {
		drumFullScale[i] = 32767;
	}
}