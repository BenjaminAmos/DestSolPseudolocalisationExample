# Destination Sol pseudo-localisation example
*See [here](https://en.wikipedia.org/wiki/Pseudolocalization) for an explanation of what pseudo-localisation actually is.*
![An image of the game's main menu, containing pseudo-localised text, such as "Ṕḽααẏ Ḡααṃḛḛ".](screenshots/MainMenuPseudolocalised.png)

This is a quick sample to demonstrate how you can replace strings in the game's assets
for a limited form of translation. Some strings are still hard-coded in the game's source
code and cannot be altered in this way.

Proper support for translations in the engine may happen in the future but this works
as a temporary work-around for now. It also serves as an example of an innovative way
in which the Gestalt asset system can be used.

You may have to change Java's default file locale to view the characters properly.
You can do this by adding `-Dfile.encoding=UTF-8` to the JVM start-up options.

## Structure
### Deltas (Overview)
The `deltas` folder contains partial alterations of certain game files. Only the changed
portions of the file are present.

As an example, the original file may look like the following:
```json
{
  "myShip": "core:smallShip",
  "hireCost": 400,
  "displayName": "Small Ship"
}
```
If you only want to change the `displayName` value, then you would include only the changed
value in the delta file. Such as this:
```json
{
  "displayName": "Small Ship with Changed Text"
}
```
### Deltas (Schemas)
The files in the `deltas/engine/schemas` folder alter the validation logic used by the engine
to check JSON files before loading them. We need to do this because the current logic
only permits ASCII-range characters in some places, rather than the full UTF-8 range.
### Overrides (Overview)
The `overrides` folder contains files that completely replace the original file content.
Due to limitations in the deltas algorithm currently, it is not possible to apply a delta
to a value within an array. You have to replace the entire file instead, using a copy
of the original.

Example of a scenario that requires an override:
```json5
{
  "type": "RelativeLayout",
  // This is the array here.
  "contents": [
    {
      "type": "UILabel",
      // The text here is within an array, so we can't apply a delta to it.
      "text": "Some Text"
    }
  ]
}
```
### Overrides (Schemas)
There is one schema containing a value in an array, so it needed to be overridden entirely.
### Overrides (Fonts)
The default Jet-Set font provided with the game only contains a subset of ASCII characters.
In order to use characters in the wider UTF-8 range, I've had to replace the game's font with
a different one (found in `overrides/engine/fonts/main.font`).

You can generate the files needed for your own font using the libGDX
[Hiero tool](https://libgdx.com/wiki/tools/hiero). The following settings should work:
```text
Font Size: 36
Padding: 0, 0, 0, 0
X Spacing: 1
Y Spacing: 1
```
The font files use a `.font` extension, instead of the tool's default `.fnt` extension.
The output `.font` file should be called `main.font`, so that it has the same asset
name as the font being overridden.

## References
- [Engine module](https://github.com/MovingBlocks/DestinationSol/tree/develop/engine/src/main/resources/org/destinationsol)
- [Core module](https://github.com/MovingBlocks/DestinationSol/tree/develop/modules/core)

## Attribution
- Overridden files taken from Destination Sol are licenced under the [Apache 2.0](https://github.com/MovingBlocks/DestinationSol/blob/develop/LICENSE) licence.
- The python script used to generate the files is based on https://github.com/Shopify/pseudolocalization. That code uses the [MIT License](https://github.com/Shopify/pseudolocalization/blob/main/LICENSE).