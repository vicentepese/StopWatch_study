// DO NOT EDIT.
//
// Generated by the Swift generator plugin for the protocol buffer compiler.
// Source: data.proto
//
// For information on using the generated types, please see the documenation:
//   https://github.com/apple/swift-protobuf/

import Foundation
import SwiftProtobuf

// If the compiler emits an error on this type, it is because this file
// was generated by a version of the `protoc` Swift plug-in that is
// incompatible with the version of SwiftProtobuf to which you are linking.
// Please ensure that your are building against the same version of the API
// that was used to generate this file.
fileprivate struct _GeneratedWithProtocGenSwiftVersion: SwiftProtobuf.ProtobufAPIVersionCheck {
  struct _2: SwiftProtobuf.ProtobufAPIVersion_2 {}
  typealias Version = _2
}

struct AccelerometerSamplesV1: SwiftProtobuf.Message {
  static let protoMessageName: String = "AccelerometerSamplesV1"

  var date: [Double] = []

  var x: [Double] = []

  var y: [Double] = []

  var z: [Double] = []

  var startDate: Double = 0

  var endDate: Double = 0

  var participantID: String = String()

  var unknownFields = SwiftProtobuf.UnknownStorage()

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    while let fieldNumber = try decoder.nextFieldNumber() {
      switch fieldNumber {
      case 1: try decoder.decodeRepeatedDoubleField(value: &self.date)
      case 2: try decoder.decodeRepeatedDoubleField(value: &self.x)
      case 3: try decoder.decodeRepeatedDoubleField(value: &self.y)
      case 4: try decoder.decodeRepeatedDoubleField(value: &self.z)
      case 5: try decoder.decodeSingularDoubleField(value: &self.startDate)
      case 6: try decoder.decodeSingularDoubleField(value: &self.endDate)
      case 7: try decoder.decodeSingularStringField(value: &self.participantID)
      default: break
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    if !self.date.isEmpty {
      try visitor.visitPackedDoubleField(value: self.date, fieldNumber: 1)
    }
    if !self.x.isEmpty {
      try visitor.visitPackedDoubleField(value: self.x, fieldNumber: 2)
    }
    if !self.y.isEmpty {
      try visitor.visitPackedDoubleField(value: self.y, fieldNumber: 3)
    }
    if !self.z.isEmpty {
      try visitor.visitPackedDoubleField(value: self.z, fieldNumber: 4)
    }
    if self.startDate != 0 {
      try visitor.visitSingularDoubleField(value: self.startDate, fieldNumber: 5)
    }
    if self.endDate != 0 {
      try visitor.visitSingularDoubleField(value: self.endDate, fieldNumber: 6)
    }
    if !self.participantID.isEmpty {
      try visitor.visitSingularStringField(value: self.participantID, fieldNumber: 7)
    }
    try unknownFields.traverse(visitor: &visitor)
  }
}

struct AccelerometerSamplesV2: SwiftProtobuf.Message {
  static let protoMessageName: String = "AccelerometerSamplesV2"

  var date: [Double] = []

  var x: [Float] = []

  var y: [Float] = []

  var z: [Float] = []

  var startDate: Double = 0

  var endDate: Double = 0

  var participantID: String = String()

  var source: AccelerometerSamplesV2.Source = .watch

  var unknownFields = SwiftProtobuf.UnknownStorage()

  /// This source field will help us distinguish
  /// between data collected on the watch and data
  /// collected on the phone.
  enum Source: SwiftProtobuf.Enum {
    typealias RawValue = Int
    case watch // = 0
    case phone // = 1
    case UNRECOGNIZED(Int)

    init() {
      self = .watch
    }

    init?(rawValue: Int) {
      switch rawValue {
      case 0: self = .watch
      case 1: self = .phone
      default: self = .UNRECOGNIZED(rawValue)
      }
    }

    var rawValue: Int {
      switch self {
      case .watch: return 0
      case .phone: return 1
      case .UNRECOGNIZED(let i): return i
      }
    }

  }

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    while let fieldNumber = try decoder.nextFieldNumber() {
      switch fieldNumber {
      case 1: try decoder.decodeRepeatedDoubleField(value: &self.date)
      case 2: try decoder.decodeRepeatedFloatField(value: &self.x)
      case 3: try decoder.decodeRepeatedFloatField(value: &self.y)
      case 4: try decoder.decodeRepeatedFloatField(value: &self.z)
      case 5: try decoder.decodeSingularDoubleField(value: &self.startDate)
      case 6: try decoder.decodeSingularDoubleField(value: &self.endDate)
      case 7: try decoder.decodeSingularStringField(value: &self.participantID)
      case 8: try decoder.decodeSingularEnumField(value: &self.source)
      default: break
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    if !self.date.isEmpty {
      try visitor.visitPackedDoubleField(value: self.date, fieldNumber: 1)
    }
    if !self.x.isEmpty {
      try visitor.visitPackedFloatField(value: self.x, fieldNumber: 2)
    }
    if !self.y.isEmpty {
      try visitor.visitPackedFloatField(value: self.y, fieldNumber: 3)
    }
    if !self.z.isEmpty {
      try visitor.visitPackedFloatField(value: self.z, fieldNumber: 4)
    }
    if self.startDate != 0 {
      try visitor.visitSingularDoubleField(value: self.startDate, fieldNumber: 5)
    }
    if self.endDate != 0 {
      try visitor.visitSingularDoubleField(value: self.endDate, fieldNumber: 6)
    }
    if !self.participantID.isEmpty {
      try visitor.visitSingularStringField(value: self.participantID, fieldNumber: 7)
    }
    if self.source != .watch {
      try visitor.visitSingularEnumField(value: self.source, fieldNumber: 8)
    }
    try unknownFields.traverse(visitor: &visitor)
  }
}

struct ActivitySamples: SwiftProtobuf.Message {
  static let protoMessageName: String = "ActivitySamples"

  var date: [Double] = []

  var stationary: [Bool] = []

  var walking: [Bool] = []

  var running: [Bool] = []

  var automotive: [Bool] = []

  var cycling: [Bool] = []

  var unknown: [Bool] = []

  var confidence: [Int32] = []

  var startDate: Double = 0

  var endDate: Double = 0

  var participantID: String = String()

  var unknownFields = SwiftProtobuf.UnknownStorage()

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    while let fieldNumber = try decoder.nextFieldNumber() {
      switch fieldNumber {
      case 1: try decoder.decodeRepeatedDoubleField(value: &self.date)
      case 2: try decoder.decodeRepeatedBoolField(value: &self.stationary)
      case 3: try decoder.decodeRepeatedBoolField(value: &self.walking)
      case 4: try decoder.decodeRepeatedBoolField(value: &self.running)
      case 5: try decoder.decodeRepeatedBoolField(value: &self.automotive)
      case 6: try decoder.decodeRepeatedBoolField(value: &self.cycling)
      case 7: try decoder.decodeRepeatedBoolField(value: &self.unknown)
      case 8: try decoder.decodeRepeatedInt32Field(value: &self.confidence)
      case 9: try decoder.decodeSingularDoubleField(value: &self.startDate)
      case 10: try decoder.decodeSingularDoubleField(value: &self.endDate)
      case 11: try decoder.decodeSingularStringField(value: &self.participantID)
      default: break
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    if !self.date.isEmpty {
      try visitor.visitPackedDoubleField(value: self.date, fieldNumber: 1)
    }
    if !self.stationary.isEmpty {
      try visitor.visitPackedBoolField(value: self.stationary, fieldNumber: 2)
    }
    if !self.walking.isEmpty {
      try visitor.visitPackedBoolField(value: self.walking, fieldNumber: 3)
    }
    if !self.running.isEmpty {
      try visitor.visitPackedBoolField(value: self.running, fieldNumber: 4)
    }
    if !self.automotive.isEmpty {
      try visitor.visitPackedBoolField(value: self.automotive, fieldNumber: 5)
    }
    if !self.cycling.isEmpty {
      try visitor.visitPackedBoolField(value: self.cycling, fieldNumber: 6)
    }
    if !self.unknown.isEmpty {
      try visitor.visitPackedBoolField(value: self.unknown, fieldNumber: 7)
    }
    if !self.confidence.isEmpty {
      try visitor.visitPackedInt32Field(value: self.confidence, fieldNumber: 8)
    }
    if self.startDate != 0 {
      try visitor.visitSingularDoubleField(value: self.startDate, fieldNumber: 9)
    }
    if self.endDate != 0 {
      try visitor.visitSingularDoubleField(value: self.endDate, fieldNumber: 10)
    }
    if !self.participantID.isEmpty {
      try visitor.visitSingularStringField(value: self.participantID, fieldNumber: 11)
    }
    try unknownFields.traverse(visitor: &visitor)
  }
}

struct FocusSession: SwiftProtobuf.Message {
  static let protoMessageName: String = "FocusSession"

  var startDate: Double {
    get {return _storage._startDate}
    set {_uniqueStorage()._startDate = newValue}
  }

  var endDate: Double {
    get {return _storage._endDate}
    set {_uniqueStorage()._endDate = newValue}
  }

  var focusRating: Float {
    get {return _storage._focusRating}
    set {_uniqueStorage()._focusRating = newValue}
  }

  var movementRating: Float {
    get {return _storage._movementRating}
    set {_uniqueStorage()._movementRating = newValue}
  }

  var participantID: String {
    get {return _storage._participantID}
    set {_uniqueStorage()._participantID = newValue}
  }

  var deviceMotion: DeviceMotion {
    get {return _storage._deviceMotion ?? DeviceMotion()}
    set {_uniqueStorage()._deviceMotion = newValue}
  }
  /// Returns true if `deviceMotion` has been explicitly set.
  var hasDeviceMotion: Bool {return _storage._deviceMotion != nil}
  /// Clears the value of `deviceMotion`. Subsequent reads from it will return its default value.
  mutating func clearDeviceMotion() {_storage._deviceMotion = nil}

  /// We record seconds from the epoch for each time
  /// the screen appears/disappears
  var screenDidAppear: [Double] {
    get {return _storage._screenDidAppear}
    set {_uniqueStorage()._screenDidAppear = newValue}
  }

  var screenWillDisappear: [Double] {
    get {return _storage._screenWillDisappear}
    set {_uniqueStorage()._screenWillDisappear = newValue}
  }

  var feedbackTime: [Double] {
    get {return _storage._feedbackTime}
    set {_uniqueStorage()._feedbackTime = newValue}
  }

  var feedback: [FocusSession.Feedback] {
    get {return _storage._feedback}
    set {_uniqueStorage()._feedback = newValue}
  }

  var unknownFields = SwiftProtobuf.UnknownStorage()

  /// We record predictions and feedback given to
  /// the user.
  enum Feedback: SwiftProtobuf.Enum {
    typealias RawValue = Int
    case focusStart // = 0
    case focusEnd // = 1
    case UNRECOGNIZED(Int)

    init() {
      self = .focusStart
    }

    init?(rawValue: Int) {
      switch rawValue {
      case 0: self = .focusStart
      case 1: self = .focusEnd
      default: self = .UNRECOGNIZED(rawValue)
      }
    }

    var rawValue: Int {
      switch self {
      case .focusStart: return 0
      case .focusEnd: return 1
      case .UNRECOGNIZED(let i): return i
      }
    }

  }

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    _ = _uniqueStorage()
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      while let fieldNumber = try decoder.nextFieldNumber() {
        switch fieldNumber {
        case 1: try decoder.decodeSingularDoubleField(value: &_storage._startDate)
        case 2: try decoder.decodeSingularDoubleField(value: &_storage._endDate)
        case 3: try decoder.decodeSingularFloatField(value: &_storage._focusRating)
        case 4: try decoder.decodeSingularStringField(value: &_storage._participantID)
        case 5: try decoder.decodeSingularFloatField(value: &_storage._movementRating)
        case 6: try decoder.decodeSingularMessageField(value: &_storage._deviceMotion)
        case 7: try decoder.decodeRepeatedDoubleField(value: &_storage._screenDidAppear)
        case 8: try decoder.decodeRepeatedDoubleField(value: &_storage._screenWillDisappear)
        case 9: try decoder.decodeRepeatedDoubleField(value: &_storage._feedbackTime)
        case 10: try decoder.decodeRepeatedEnumField(value: &_storage._feedback)
        default: break
        }
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      if _storage._startDate != 0 {
        try visitor.visitSingularDoubleField(value: _storage._startDate, fieldNumber: 1)
      }
      if _storage._endDate != 0 {
        try visitor.visitSingularDoubleField(value: _storage._endDate, fieldNumber: 2)
      }
      if _storage._focusRating != 0 {
        try visitor.visitSingularFloatField(value: _storage._focusRating, fieldNumber: 3)
      }
      if !_storage._participantID.isEmpty {
        try visitor.visitSingularStringField(value: _storage._participantID, fieldNumber: 4)
      }
      if _storage._movementRating != 0 {
        try visitor.visitSingularFloatField(value: _storage._movementRating, fieldNumber: 5)
      }
      if let v = _storage._deviceMotion {
        try visitor.visitSingularMessageField(value: v, fieldNumber: 6)
      }
      if !_storage._screenDidAppear.isEmpty {
        try visitor.visitPackedDoubleField(value: _storage._screenDidAppear, fieldNumber: 7)
      }
      if !_storage._screenWillDisappear.isEmpty {
        try visitor.visitPackedDoubleField(value: _storage._screenWillDisappear, fieldNumber: 8)
      }
      if !_storage._feedbackTime.isEmpty {
        try visitor.visitPackedDoubleField(value: _storage._feedbackTime, fieldNumber: 9)
      }
      if !_storage._feedback.isEmpty {
        try visitor.visitPackedEnumField(value: _storage._feedback, fieldNumber: 10)
      }
    }
    try unknownFields.traverse(visitor: &visitor)
  }

  fileprivate var _storage = _StorageClass.defaultInstance
}

/// This message is used to hold a sequence of samples of a 3-vector.
/// We use this class when storing DeviceMotion.
struct VectorSamples: SwiftProtobuf.Message {
  static let protoMessageName: String = "VectorSamples"

  var x: [Float] = []

  var y: [Float] = []

  var z: [Float] = []

  var unknownFields = SwiftProtobuf.UnknownStorage()

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    while let fieldNumber = try decoder.nextFieldNumber() {
      switch fieldNumber {
      case 1: try decoder.decodeRepeatedFloatField(value: &self.x)
      case 2: try decoder.decodeRepeatedFloatField(value: &self.y)
      case 3: try decoder.decodeRepeatedFloatField(value: &self.z)
      default: break
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    if !self.x.isEmpty {
      try visitor.visitPackedFloatField(value: self.x, fieldNumber: 1)
    }
    if !self.y.isEmpty {
      try visitor.visitPackedFloatField(value: self.y, fieldNumber: 2)
    }
    if !self.z.isEmpty {
      try visitor.visitPackedFloatField(value: self.z, fieldNumber: 3)
    }
    try unknownFields.traverse(visitor: &visitor)
  }
}

struct DeviceMotion: SwiftProtobuf.Message {
  static let protoMessageName: String = "DeviceMotion"

  var userAcceleration: VectorSamples {
    get {return _storage._userAcceleration ?? VectorSamples()}
    set {_uniqueStorage()._userAcceleration = newValue}
  }
  /// Returns true if `userAcceleration` has been explicitly set.
  var hasUserAcceleration: Bool {return _storage._userAcceleration != nil}
  /// Clears the value of `userAcceleration`. Subsequent reads from it will return its default value.
  mutating func clearUserAcceleration() {_storage._userAcceleration = nil}

  var rotationRate: VectorSamples {
    get {return _storage._rotationRate ?? VectorSamples()}
    set {_uniqueStorage()._rotationRate = newValue}
  }
  /// Returns true if `rotationRate` has been explicitly set.
  var hasRotationRate: Bool {return _storage._rotationRate != nil}
  /// Clears the value of `rotationRate`. Subsequent reads from it will return its default value.
  mutating func clearRotationRate() {_storage._rotationRate = nil}

  var gravity: VectorSamples {
    get {return _storage._gravity ?? VectorSamples()}
    set {_uniqueStorage()._gravity = newValue}
  }
  /// Returns true if `gravity` has been explicitly set.
  var hasGravity: Bool {return _storage._gravity != nil}
  /// Clears the value of `gravity`. Subsequent reads from it will return its default value.
  mutating func clearGravity() {_storage._gravity = nil}

  var date: [Double] {
    get {return _storage._date}
    set {_uniqueStorage()._date = newValue}
  }

  /// Data from CMAttitude
  var attitudeRoll: [Float] {
    get {return _storage._attitudeRoll}
    set {_uniqueStorage()._attitudeRoll = newValue}
  }

  var attitudePitch: [Float] {
    get {return _storage._attitudePitch}
    set {_uniqueStorage()._attitudePitch = newValue}
  }

  var attitudeYaw: [Float] {
    get {return _storage._attitudeYaw}
    set {_uniqueStorage()._attitudeYaw = newValue}
  }

  var heading: [Float] {
    get {return _storage._heading}
    set {_uniqueStorage()._heading = newValue}
  }

  var unknownFields = SwiftProtobuf.UnknownStorage()

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    _ = _uniqueStorage()
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      while let fieldNumber = try decoder.nextFieldNumber() {
        switch fieldNumber {
        case 1: try decoder.decodeSingularMessageField(value: &_storage._userAcceleration)
        case 2: try decoder.decodeSingularMessageField(value: &_storage._rotationRate)
        case 3: try decoder.decodeSingularMessageField(value: &_storage._gravity)
        case 4: try decoder.decodeRepeatedDoubleField(value: &_storage._date)
        case 5: try decoder.decodeRepeatedFloatField(value: &_storage._attitudeRoll)
        case 6: try decoder.decodeRepeatedFloatField(value: &_storage._attitudePitch)
        case 7: try decoder.decodeRepeatedFloatField(value: &_storage._attitudeYaw)
        case 8: try decoder.decodeRepeatedFloatField(value: &_storage._heading)
        default: break
        }
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      if let v = _storage._userAcceleration {
        try visitor.visitSingularMessageField(value: v, fieldNumber: 1)
      }
      if let v = _storage._rotationRate {
        try visitor.visitSingularMessageField(value: v, fieldNumber: 2)
      }
      if let v = _storage._gravity {
        try visitor.visitSingularMessageField(value: v, fieldNumber: 3)
      }
      if !_storage._date.isEmpty {
        try visitor.visitPackedDoubleField(value: _storage._date, fieldNumber: 4)
      }
      if !_storage._attitudeRoll.isEmpty {
        try visitor.visitPackedFloatField(value: _storage._attitudeRoll, fieldNumber: 5)
      }
      if !_storage._attitudePitch.isEmpty {
        try visitor.visitPackedFloatField(value: _storage._attitudePitch, fieldNumber: 6)
      }
      if !_storage._attitudeYaw.isEmpty {
        try visitor.visitPackedFloatField(value: _storage._attitudeYaw, fieldNumber: 7)
      }
      if !_storage._heading.isEmpty {
        try visitor.visitPackedFloatField(value: _storage._heading, fieldNumber: 8)
      }
    }
    try unknownFields.traverse(visitor: &visitor)
  }

  fileprivate var _storage = _StorageClass.defaultInstance
}

struct PhoneFocusSession: SwiftProtobuf.Message {
  static let protoMessageName: String = "PhoneFocusSession"

  var startDate: Double {
    get {return _storage._startDate}
    set {_uniqueStorage()._startDate = newValue}
  }

  var endDate: Double {
    get {return _storage._endDate}
    set {_uniqueStorage()._endDate = newValue}
  }

  var participantID: String {
    get {return _storage._participantID}
    set {_uniqueStorage()._participantID = newValue}
  }

  var deviceMotion: DeviceMotion {
    get {return _storage._deviceMotion ?? DeviceMotion()}
    set {_uniqueStorage()._deviceMotion = newValue}
  }
  /// Returns true if `deviceMotion` has been explicitly set.
  var hasDeviceMotion: Bool {return _storage._deviceMotion != nil}
  /// Clears the value of `deviceMotion`. Subsequent reads from it will return its default value.
  mutating func clearDeviceMotion() {_storage._deviceMotion = nil}

  var unknownFields = SwiftProtobuf.UnknownStorage()

  init() {}

  /// Used by the decoding initializers in the SwiftProtobuf library, not generally
  /// used directly. `init(serializedData:)`, `init(jsonUTF8Data:)`, and other decoding
  /// initializers are defined in the SwiftProtobuf library. See the Message and
  /// Message+*Additions` files.
  mutating func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    _ = _uniqueStorage()
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      while let fieldNumber = try decoder.nextFieldNumber() {
        switch fieldNumber {
        case 1: try decoder.decodeSingularDoubleField(value: &_storage._startDate)
        case 2: try decoder.decodeSingularDoubleField(value: &_storage._endDate)
        case 3: try decoder.decodeSingularStringField(value: &_storage._participantID)
        case 4: try decoder.decodeSingularMessageField(value: &_storage._deviceMotion)
        default: break
        }
      }
    }
  }

  /// Used by the encoding methods of the SwiftProtobuf library, not generally
  /// used directly. `Message.serializedData()`, `Message.jsonUTF8Data()`, and
  /// other serializer methods are defined in the SwiftProtobuf library. See the
  /// `Message` and `Message+*Additions` files.
  func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    try withExtendedLifetime(_storage) { (_storage: _StorageClass) in
      if _storage._startDate != 0 {
        try visitor.visitSingularDoubleField(value: _storage._startDate, fieldNumber: 1)
      }
      if _storage._endDate != 0 {
        try visitor.visitSingularDoubleField(value: _storage._endDate, fieldNumber: 2)
      }
      if !_storage._participantID.isEmpty {
        try visitor.visitSingularStringField(value: _storage._participantID, fieldNumber: 3)
      }
      if let v = _storage._deviceMotion {
        try visitor.visitSingularMessageField(value: v, fieldNumber: 4)
      }
    }
    try unknownFields.traverse(visitor: &visitor)
  }

  fileprivate var _storage = _StorageClass.defaultInstance
}

// MARK: - Code below here is support for the SwiftProtobuf runtime.

extension AccelerometerSamplesV1: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .same(proto: "date"),
    2: .same(proto: "x"),
    3: .same(proto: "y"),
    4: .same(proto: "z"),
    5: .standard(proto: "start_date"),
    6: .standard(proto: "end_date"),
    7: .standard(proto: "participant_id"),
  ]

  func _protobuf_generated_isEqualTo(other: AccelerometerSamplesV1) -> Bool {
    if self.date != other.date {return false}
    if self.x != other.x {return false}
    if self.y != other.y {return false}
    if self.z != other.z {return false}
    if self.startDate != other.startDate {return false}
    if self.endDate != other.endDate {return false}
    if self.participantID != other.participantID {return false}
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension AccelerometerSamplesV2: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .same(proto: "date"),
    2: .same(proto: "x"),
    3: .same(proto: "y"),
    4: .same(proto: "z"),
    5: .standard(proto: "start_date"),
    6: .standard(proto: "end_date"),
    7: .standard(proto: "participant_id"),
    8: .same(proto: "source"),
  ]

  func _protobuf_generated_isEqualTo(other: AccelerometerSamplesV2) -> Bool {
    if self.date != other.date {return false}
    if self.x != other.x {return false}
    if self.y != other.y {return false}
    if self.z != other.z {return false}
    if self.startDate != other.startDate {return false}
    if self.endDate != other.endDate {return false}
    if self.participantID != other.participantID {return false}
    if self.source != other.source {return false}
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension AccelerometerSamplesV2.Source: SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    0: .same(proto: "WATCH"),
    1: .same(proto: "PHONE"),
  ]
}

extension ActivitySamples: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .same(proto: "date"),
    2: .same(proto: "stationary"),
    3: .same(proto: "walking"),
    4: .same(proto: "running"),
    5: .same(proto: "automotive"),
    6: .same(proto: "cycling"),
    7: .same(proto: "unknown"),
    8: .same(proto: "confidence"),
    9: .standard(proto: "start_date"),
    10: .standard(proto: "end_date"),
    11: .standard(proto: "participant_id"),
  ]

  func _protobuf_generated_isEqualTo(other: ActivitySamples) -> Bool {
    if self.date != other.date {return false}
    if self.stationary != other.stationary {return false}
    if self.walking != other.walking {return false}
    if self.running != other.running {return false}
    if self.automotive != other.automotive {return false}
    if self.cycling != other.cycling {return false}
    if self.unknown != other.unknown {return false}
    if self.confidence != other.confidence {return false}
    if self.startDate != other.startDate {return false}
    if self.endDate != other.endDate {return false}
    if self.participantID != other.participantID {return false}
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension FocusSession: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .standard(proto: "start_date"),
    2: .standard(proto: "end_date"),
    3: .standard(proto: "focus_rating"),
    5: .standard(proto: "movement_rating"),
    4: .standard(proto: "participant_id"),
    6: .standard(proto: "device_motion"),
    7: .standard(proto: "screen_did_appear"),
    8: .standard(proto: "screen_will_disappear"),
    9: .standard(proto: "feedback_time"),
    10: .same(proto: "feedback"),
  ]

  fileprivate class _StorageClass {
    var _startDate: Double = 0
    var _endDate: Double = 0
    var _focusRating: Float = 0
    var _movementRating: Float = 0
    var _participantID: String = String()
    var _deviceMotion: DeviceMotion? = nil
    var _screenDidAppear: [Double] = []
    var _screenWillDisappear: [Double] = []
    var _feedbackTime: [Double] = []
    var _feedback: [FocusSession.Feedback] = []

    static let defaultInstance = _StorageClass()

    private init() {}

    init(copying source: _StorageClass) {
      _startDate = source._startDate
      _endDate = source._endDate
      _focusRating = source._focusRating
      _movementRating = source._movementRating
      _participantID = source._participantID
      _deviceMotion = source._deviceMotion
      _screenDidAppear = source._screenDidAppear
      _screenWillDisappear = source._screenWillDisappear
      _feedbackTime = source._feedbackTime
      _feedback = source._feedback
    }
  }

  fileprivate mutating func _uniqueStorage() -> _StorageClass {
    if !isKnownUniquelyReferenced(&_storage) {
      _storage = _StorageClass(copying: _storage)
    }
    return _storage
  }

  func _protobuf_generated_isEqualTo(other: FocusSession) -> Bool {
    if _storage !== other._storage {
      let storagesAreEqual: Bool = withExtendedLifetime((_storage, other._storage)) { (_args: (_StorageClass, _StorageClass)) in
        let _storage = _args.0
        let other_storage = _args.1
        if _storage._startDate != other_storage._startDate {return false}
        if _storage._endDate != other_storage._endDate {return false}
        if _storage._focusRating != other_storage._focusRating {return false}
        if _storage._movementRating != other_storage._movementRating {return false}
        if _storage._participantID != other_storage._participantID {return false}
        if _storage._deviceMotion != other_storage._deviceMotion {return false}
        if _storage._screenDidAppear != other_storage._screenDidAppear {return false}
        if _storage._screenWillDisappear != other_storage._screenWillDisappear {return false}
        if _storage._feedbackTime != other_storage._feedbackTime {return false}
        if _storage._feedback != other_storage._feedback {return false}
        return true
      }
      if !storagesAreEqual {return false}
    }
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension FocusSession.Feedback: SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    0: .same(proto: "FOCUS_START"),
    1: .same(proto: "FOCUS_END"),
  ]
}

extension VectorSamples: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .same(proto: "x"),
    2: .same(proto: "y"),
    3: .same(proto: "z"),
  ]

  func _protobuf_generated_isEqualTo(other: VectorSamples) -> Bool {
    if self.x != other.x {return false}
    if self.y != other.y {return false}
    if self.z != other.z {return false}
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension DeviceMotion: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .standard(proto: "user_acceleration"),
    2: .standard(proto: "rotation_rate"),
    3: .same(proto: "gravity"),
    4: .same(proto: "date"),
    5: .standard(proto: "attitude_roll"),
    6: .standard(proto: "attitude_pitch"),
    7: .standard(proto: "attitude_yaw"),
    8: .same(proto: "heading"),
  ]

  fileprivate class _StorageClass {
    var _userAcceleration: VectorSamples? = nil
    var _rotationRate: VectorSamples? = nil
    var _gravity: VectorSamples? = nil
    var _date: [Double] = []
    var _attitudeRoll: [Float] = []
    var _attitudePitch: [Float] = []
    var _attitudeYaw: [Float] = []
    var _heading: [Float] = []

    static let defaultInstance = _StorageClass()

    private init() {}

    init(copying source: _StorageClass) {
      _userAcceleration = source._userAcceleration
      _rotationRate = source._rotationRate
      _gravity = source._gravity
      _date = source._date
      _attitudeRoll = source._attitudeRoll
      _attitudePitch = source._attitudePitch
      _attitudeYaw = source._attitudeYaw
      _heading = source._heading
    }
  }

  fileprivate mutating func _uniqueStorage() -> _StorageClass {
    if !isKnownUniquelyReferenced(&_storage) {
      _storage = _StorageClass(copying: _storage)
    }
    return _storage
  }

  func _protobuf_generated_isEqualTo(other: DeviceMotion) -> Bool {
    if _storage !== other._storage {
      let storagesAreEqual: Bool = withExtendedLifetime((_storage, other._storage)) { (_args: (_StorageClass, _StorageClass)) in
        let _storage = _args.0
        let other_storage = _args.1
        if _storage._userAcceleration != other_storage._userAcceleration {return false}
        if _storage._rotationRate != other_storage._rotationRate {return false}
        if _storage._gravity != other_storage._gravity {return false}
        if _storage._date != other_storage._date {return false}
        if _storage._attitudeRoll != other_storage._attitudeRoll {return false}
        if _storage._attitudePitch != other_storage._attitudePitch {return false}
        if _storage._attitudeYaw != other_storage._attitudeYaw {return false}
        if _storage._heading != other_storage._heading {return false}
        return true
      }
      if !storagesAreEqual {return false}
    }
    if unknownFields != other.unknownFields {return false}
    return true
  }
}

extension PhoneFocusSession: SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
  static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .standard(proto: "start_date"),
    2: .standard(proto: "end_date"),
    3: .standard(proto: "participant_id"),
    4: .standard(proto: "device_motion"),
  ]

  fileprivate class _StorageClass {
    var _startDate: Double = 0
    var _endDate: Double = 0
    var _participantID: String = String()
    var _deviceMotion: DeviceMotion? = nil

    static let defaultInstance = _StorageClass()

    private init() {}

    init(copying source: _StorageClass) {
      _startDate = source._startDate
      _endDate = source._endDate
      _participantID = source._participantID
      _deviceMotion = source._deviceMotion
    }
  }

  fileprivate mutating func _uniqueStorage() -> _StorageClass {
    if !isKnownUniquelyReferenced(&_storage) {
      _storage = _StorageClass(copying: _storage)
    }
    return _storage
  }

  func _protobuf_generated_isEqualTo(other: PhoneFocusSession) -> Bool {
    if _storage !== other._storage {
      let storagesAreEqual: Bool = withExtendedLifetime((_storage, other._storage)) { (_args: (_StorageClass, _StorageClass)) in
        let _storage = _args.0
        let other_storage = _args.1
        if _storage._startDate != other_storage._startDate {return false}
        if _storage._endDate != other_storage._endDate {return false}
        if _storage._participantID != other_storage._participantID {return false}
        if _storage._deviceMotion != other_storage._deviceMotion {return false}
        return true
      }
      if !storagesAreEqual {return false}
    }
    if unknownFields != other.unknownFields {return false}
    return true
  }
}
