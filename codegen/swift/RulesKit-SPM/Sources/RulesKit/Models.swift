import Foundation

public struct StaffSpace: Codable { public var value: Double }

public struct BBox: Codable {
    public var x: Double
    public var y: Double
    public var w: Double
    public var h: Double
    public init(x: Double, y: Double, w: Double, h: Double) {
        self.x = x; self.y = y; self.w = w; self.h = h
    }
}

public struct BeamSegment: Codable {
    public var x1: Double
    public var y1: Double
    public var x2: Double
    public var y2: Double
    public init(x1: Double, y1: Double, x2: Double, y2: Double) {
        self.x1 = x1; self.y1 = y1; self.x2 = x2; self.y2 = y2
    }
}

// MARK: - Collision: Beams
public struct BeamCollisionInput: Codable {
    public var beamSegments: [BeamSegment]
    public var nearbyGrobs: [BBox]
}
public struct BeamCollisionOutput: Codable {
    public var offsets: [Double]
}

// MARK: - Collision: Rests
public struct RestCollisionInput: Codable {
    public var restBBoxes: [BBox]
    public var noteColumnBBoxes: [BBox]
}
public struct RestCollisionOutput: Codable {
    public struct Offset: Codable { public var x: Double; public var y: Double }
    public var restOffsets: [Offset]
}

// MARK: - Dynamics: Kerning with hairpins/lyrics
public struct DynamicKerningInput: Codable {
    public var dynamicBBox: BBox
    public var hairpinBBox: BBox?
    public var lyricBBox: BBox?
}
public struct DynamicKerningOutput: Codable {
    public struct Position: Codable { public var x: Double; public var y: Double }
    public var dynamicPosition: Position
}

// MARK: - Beaming: slope with clearance
public struct BeamingSlopeClearanceInput: Codable {
    public var notePositionsSP: [Double]
    public var stemDirections: [String] // "up" | "down"
    public var beamThicknessSP: Double
    public var nearbyGrobs: [BBox]?
}
public struct BeamingSlopeClearanceOutput: Codable {
    public var slopeSPPerSpaceAdjusted: Double
    public var minClearanceSP: Double?
}

// MARK: - Spacing: optical stem weights
public struct NoteSpacingOpticalWeightsInput: Codable {
    public var stemDirections: [String]
    public var beatStrengths: [Double]
}
public struct NoteSpacingOpticalWeightsOutput: Codable {
    public var weights: [Double]
}

// MARK: - Lyrics: baseline variance
public struct LyricsBaselineVarianceInput: Codable {
    public var lyricBBox: BBox
    public var staffBaseline: Double
    public var varianceSP: Double?
}
public struct LyricsBaselineVarianceOutput: Codable {
    public var yOffsetSP: Double
}

// MARK: - Beaming: cross voice mixed-stem
public struct BeamingCrossVoiceSlopeInput: Codable {
    public var voiceNotePositionsSP: [[Double]]
    public var voiceStemDirections: [[String]]
    public var beamThicknessSP: Double
}
public struct BeamingCrossVoiceSlopeOutput: Codable {
    public var slopeSPPerSpaceAdjusted: Double
    public var balanceScore: Double
}

// MARK: - Dynamics: stacked kerning
public struct DynamicsStackKerningInput: Codable {
    public var dynamicBBoxes: [BBox]
    public var hairpinBBoxes: [BBox]?
    public var atSystemBreak: Bool?
}
public struct DynamicsStackKerningOutput: Codable {
    public struct Position: Codable { public var x: Double; public var y: Double }
    public var dynamicPositions: [Position]
}

// MARK: - Lyrics: hyphen & melisma
public struct LyricsHyphenMelismaInput: Codable {
    public var syllableBBoxes: [BBox]
    public var hyphenBBoxes: [BBox]?
    public var melismaLineBBoxes: [BBox]?
    public var staffBaseline: Double
}
public struct LyricsHyphenMelismaOutput: Codable {
    public var lyricOffsets: [Double]
    public var baselineYOffsetSP: Double?
}

