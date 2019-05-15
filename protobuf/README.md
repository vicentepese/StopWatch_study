# Using protobufs

Protobufs are an efficient, explicit data serialization format developed and used by Google. We check in compiled classes to this repo to make building the project a bit easier, so you only need to set up protobufs if you want to change the serialization format. Do this carefully, and avoid changing the identifiers of fields.

### Setup your environment to build protos
You might need to make sure you have Xcode Command Line Tools set up for this to work.
```bash
brew install protobuf
cd $PROJECT_ROOT/Frameworks/swift-protobuf
swift build -c release -Xswiftc -static-stdlib
```
You'll need to find a way to get the file `./.build/release/protoc-gen-swift` into your path. You can copy this to a directory that is in your path or do something like
```bash
export PATH=$PATH:$PROJECT_ROOT/Frameworks/swift-protobuf/.build/release
```

### Building protos
```bash
cd $PROJECT_ROOT
./protobuf/build.sh
```
