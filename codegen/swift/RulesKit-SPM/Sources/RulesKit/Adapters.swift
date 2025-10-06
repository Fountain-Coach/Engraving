import Foundation

public extension RulesKitClient {
    // Collision: Beams
    func resolveBeamCollisions(_ input: BeamCollisionInput) async throws -> BeamCollisionOutput {
        try await post("apply/collision/BeamCollision-resolve_overlaps", input)
    }
    // Collision: Rests
    func resolveRestCollisions(_ input: RestCollisionInput) async throws -> RestCollisionOutput {
        try await post("apply/collision/RestCollision-resolve_overlaps", input)
    }
    // Dynamics: kerning with hairpins/lyrics
    func dynamicKerning(_ input: DynamicKerningInput) async throws -> DynamicKerningOutput {
        try await post("apply/dynamicstext/DynamicAlign-kerning_with_hairpins", input)
    }
    // Beaming: slope with clearance
    func beamingSlopeWithClearance(_ input: BeamingSlopeClearanceInput) async throws -> BeamingSlopeClearanceOutput {
        try await post("apply/beaming/Beaming-slope_with_clearance", input)
    }
    // Spacing: optical weights
    func noteSpacingOpticalWeights(_ input: NoteSpacingOpticalWeightsInput) async throws -> NoteSpacingOpticalWeightsOutput {
        try await post("apply/spacing/NoteSpacing-optical_stem_weight_scalars", input)
    }
    // Lyrics: baseline variance
    func lyricsBaselineVariance(_ input: LyricsBaselineVarianceInput) async throws -> LyricsBaselineVarianceOutput {
        try await post("apply/verticalstack/Lyrics-baseline_adjustment_with_variance", input)
    }
    // Beaming: cross-voice mixed-stem balance
    func beamingCrossVoiceMixedStem(_ input: BeamingCrossVoiceSlopeInput) async throws -> BeamingCrossVoiceSlopeOutput {
        try await post("apply/beaming/Beaming-cross_voice_mixed_stem_slope_balance", input)
    }
    // Dynamics: stacked kerning
    func dynamicsStackedKerning(_ input: DynamicsStackKerningInput) async throws -> DynamicsStackKerningOutput {
        try await post("apply/dynamicstext/Dynamics-stacked_kerning_with_system_breaks", input)
    }
    // Lyrics: hyphen & melisma interaction
    func lyricsHyphenMelisma(_ input: LyricsHyphenMelismaInput) async throws -> LyricsHyphenMelismaOutput {
        try await post("apply/verticalstack/Lyrics-hyphen_melisma_spacing_interaction", input)
    }
}

