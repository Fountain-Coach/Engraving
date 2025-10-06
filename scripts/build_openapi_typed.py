#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
UNTYPED = ROOT / 'openapi' / 'rules-as-functions.yaml'
TYPED = ROOT / 'openapi' / 'rules-as-functions.typed.yaml'

def ensure_components(doc):
    comp = doc.setdefault('components', {}).setdefault('schemas', {})
    # Keep legacy placeholders present but unused to avoid KeyErrors.
    comp.setdefault('RuleInput', { 'type': 'object', 'additionalProperties': False, 'properties': {} })
    comp.setdefault('RuleOutput', { 'type': 'object', 'additionalProperties': False, 'properties': {} })
    # Provide a generic typed fallback so we never emit RuleInput/RuleOutput.
    comp.setdefault('StrictEmpty', { 'type': 'object', 'additionalProperties': False })

def main():
    untyped = yaml.safe_load(UNTYPED.read_text())
    typed = yaml.safe_load(TYPED.read_text())
    ensure_components(typed)
    tpaths = typed.setdefault('paths', {})
    upaths = untyped.get('paths', {})
    # Prune typed paths that no longer exist in untyped (keeps specs in lockstep)
    extra = set(tpaths.keys()) - set(upaths.keys())
    for p in sorted(extra):
        del tpaths[p]
    # Known typed schema mappings by rule id
    schema_map = {
        'RULE.Spacing.duration_base_with_optical_corrections': ('SpacingDurationBaseInput','SpacingDurationBaseOutput'),
        'RULE.Spacing.keep_inside_system_constraints': ('KeepInsideInput','KeepInsideOutput'),
        'RULE.Beaming.auto_knee_threshold': ('BeamingKneeInput','BeamingKneeOutput'),
        'RULE.Beaming.compound_meter_grouping': ('CompoundBeamingInput','CompoundBeamingOutput'),
        'RULE.Beaming.geometry_slope_and_segments': ('BeamGeometryInput','BeamGeometryOutput'),
        'RULE.Beaming.rests_split_groups': ('RestSplitInput','RestSplitOutput'),
        'RULE.Beaming.subdivision_preference': ('BeamingSubdivisionInput','BeamingSubdivisionOutput'),
        'RULE.Slur.curvature_choice_with_collision_penalty': ('SlurInput','SlurOutput'),
        'RULE.Tie.curvature_selection_with_clearance': ('TieCurvatureInput','TieCurvatureOutput'),
        'RULE.Collision.priority_lattice': ('CollisionLatticeInput','CollisionLatticeOutput'),
        'RULE.Accidental.leading_padding_and_column_inflation': ('AccidentalLeadInInput','AccidentalLeadInOutput'),
        'RULE.Accidental.cautionary_parenthesized_policy': ('AccidentalCautionaryInput','AccidentalCautionaryOutput'),
        'RULE.Accidental.microtonal_glyph_selection_and_spacing': ('AccidentalMicrotonalInput','AccidentalMicrotonalOutput'),
        'RULE.Clef.mid_system_placement': ('ClefPlacementInput','ClefPlacementOutput'),
        'RULE.KeySignature.courtesy_at_line_breaks': ('CourtesyKeyInput','CourtesyKeyOutput'),
        'RULE.TimeSignature.courtesy_at_line_breaks': ('CourtesyTimeInput','CourtesyTimeOutput'),
        'RULE.Lyrics.vertical_alignment_with_baselines': ('LyricsAlignInput','LyricsAlignOutput'),
        'RULE.Ornaments.placement_above_below_with_collision': ('OrnamentPlacementInput','OrnamentPlacementOutput'),
        'RULE.PartStaff.braces_brackets_layout': ('BracesLayoutInput','BracesLayoutOutput'),
        'RULE.MultiVoice.stem_directions_up_down': ('MultiVoiceStemsInput','MultiVoiceStemsOutput'),
        'RULE.Pagination.castoff_fill_vs_overfull_penalties': ('CastoffInput','CastoffOutput'),
        'RULE.OpticalSize.stroke_and_spacing_scalars': ('StrictEmpty','StrictEmpty'),
        'RULE.Arpeggio.placement_policy': ('ArpeggioPlacementInput','ArpeggioPlacementOutput'),
        'RULE.Fingering.placement_policy': ('FingeringPlacementInput','FingeringPlacementOutput'),
        'RULE.Pedal.line_and_text_policy': ('PedalPlacementInput','PedalPlacementOutput'),
        'RULE.TrillSpanner.placement_policy': ('TrillPlacementInput','TrillPlacementOutput'),
        'RULE.Ottava.placement_policy': ('OttavaPlacementInput','OttavaPlacementOutput'),
        'RULE.RehearsalMarks.placement_policy': ('RehearsalPlacementInput','RehearsalPlacementOutput'),
        'RULE.TempoMarks.placement_policy': ('TempoPlacementInput','TempoPlacementOutput'),
        'RULE.Ledger.shorten_near_accidental': ('LedgerShortenInput','LedgerShortenOutput'),
        'RULE.Vertical.min_dist_padding_and_stretch': ('VerticalStackInput','VerticalStackOutput'),
        'RULE.Dynamics.align_with_noteheads_and_stems': ('DynamicsAlignInput','DynamicsAlignOutput'),
        'RULE.BeamCollision.resolve_overlaps': ('BeamCollisionInput','BeamCollisionOutput'),
        'RULE.RestCollision.resolve_overlaps': ('RestCollisionInput','RestCollisionOutput'),
        'RULE.Dynamics.stacked_kerning_with_system_breaks': ('DynamicsStackKerningInput','DynamicsStackKerningOutput'),
        'RULE.Lyrics.hyphen_melisma_spacing_interaction': ('LyricsHyphenMelismaInput','LyricsHyphenMelismaOutput'),
        'RULE.Lyrics.extender_spacing_policy': ('LyricsExtenderInput','LyricsExtenderOutput'),
        'RULE.InstrumentSwitch.placement_policy': ('InstrumentSwitchInput','InstrumentSwitchOutput'),
        'RULE.LigatureBracket.placement_policy': ('LigatureBracketInput','LigatureBracketOutput'),
        'RULE.NonMusicalScriptColumn.layout_policy': ('NonMusicalScriptColumnInput','NonMusicalScriptColumnOutput'),
        'RULE.OutputProperty.override_inheritance_policy': ('OutputPropertyOverrideInput','OutputPropertyOverrideOutput'),
        'RULE.PitchedTrill.placement_policy': ('PitchedTrillInput','PitchedTrillOutput'),
        'RULE.ScriptColumn.layout_policy': ('ScriptColumnInput','ScriptColumnOutput'),
        'RULE.ScriptRow.layout_policy': ('ScriptRowInput','ScriptRowOutput'),
        'RULE.SpanArpeggio.placement_policy': ('SpanArpeggioInput','SpanArpeggioOutput'),
        'RULE.HorizontalBracket.placement_policy': ('HorizontalBracketInput','HorizontalBracketOutput'),
        'RULE.Text.placement_policy': ('TextPlacementInput','TextPlacementOutput'),
        'RULE.PercentRepeat.layout_policy': ('StrictEmpty','StrictEmpty'),
        'RULE.SlashRepeat.layout_policy': ('StrictEmpty','StrictEmpty'),
        'RULE.SystemStartDelimiter.layout_policy': ('StrictEmpty','StrictEmpty'),
    }

    for path, op in upaths.items():
        rid = op['post']['operationId']
        if path not in tpaths:
            newpost = {
                'operationId': rid,
                'summary': op['post'].get('summary',''),
                'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/StrictEmpty'}}}},
                'responses': {'200': {'description': 'OK', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/StrictEmpty'}}}}}
            }
            # Copy vendor extensions (x-rule, x-smufl) from untyped where present
            for xkey in ('x-rule','x-smufl'):
                if xkey in op['post']:
                    newpost[xkey] = op['post'][xkey]
            tpaths[path] = {'post': newpost}
        # Ensure vendor extensions are present for existing paths
        post = tpaths[path]['post']
        for xkey in ('x-rule','x-smufl'):
            if xkey in op['post']:
                post[xkey] = op['post'][xkey]
        # Replace StrictEmpty with concrete typed schemas when mapping exists
        if rid in schema_map:
            req, res = schema_map[rid]
            if req:
                post['requestBody'] = {'required': True, 'content': {'application/json': {'schema': {'$ref': f"#/components/schemas/{req}"}}}}
            if res:
                post['responses'] = {'200': {'description': op['post'].get('responses',{}).get('200',{}).get('description','OK'), 'content': {'application/json': {'schema': {'$ref': f"#/components/schemas/{res}"}}}}}
    TYPED.write_text(yaml.safe_dump(typed, sort_keys=False))
    print('Typed OpenAPI updated with parity for all rules (placeholders for new ops).')

if __name__ == '__main__':
    main()
