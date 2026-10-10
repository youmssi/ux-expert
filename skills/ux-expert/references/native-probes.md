# Native mobile probes

<!-- Generated from criteria/probes.yaml by scripts/generate.py. Edit the YAML, then run the script. -->

Code search probes for iOS, Android, Flutter and React Native, used in recon (`references/codebase-recon.md`)
and by the areas that cite them. Run them all at once with `python3 scripts/probe.py <project root>`, or
search one pattern with Grep or `rg`. A hit is a place to look, never a finding by itself: open the code and
check it against the criterion before reporting. In the tables, `\|` is an escaped `|`; `probe.py` and
`criteria/catalogue.json` carry the raw patterns.

Kinds: **inventory**: locate and count; **review**: each hit needs a look, often fine; **smell**: usually a defect; confirm before reporting.

## iOS (SwiftUI, UIKit)

Files: `.swift` · detected by any .swift file · sources: [src:apple-swiftui-docs], [src:apple-hig-targets]

- `Text("Save")` with a literal is a `LocalizedStringKey`: SwiftUI looks it up in the string catalog. Hard-coded strings are not a defect by themselves; check that a catalog exists and covers them.
- `Image("hero")` takes its accessibility label from the asset name. Check the name reads well, or use `Image(decorative:)` for decoration.
- Targets are 44 × 44 pt; a smaller visible control is fine when `.contentShape` or padding gives it a larger tappable area.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `ios-screens` | inventory | `NavigationStack\|NavigationSplitView\|NavigationView\|TabView\|\.sheet\(\|\.fullScreenCover\(\|class \w+: UIViewController` | Screens and overlays for the surface map. | — |
| `ios-fixed-font-size` | smell | `\.system\(size:\|\.custom\([^)]*fixedSize:\|UIFont\.(systemFont\|boldSystemFont)\(ofSize:` | Text that ignores Dynamic Type. Text styles (`.body`) and `.custom(_:size:)` scale; `.system(size:)`, `fixedSize:` and UIKit fonts without `UIFontMetrics` do not. | TYP-10, A11Y-32, RESP-12 |
| `ios-dynamic-type-limit` | review | `\.dynamicTypeSize\(` | A cap on Dynamic Type. Acceptable on compact chrome; a defect on body content. | TYP-10, A11Y-32 |
| `ios-tap-gesture` | smell | `\.onTapGesture` | A tappable view that is not a `Button`. VoiceOver gets no button trait unless `.accessibilityAddTraits(.isButton)` is added, and there is no pressed state. | A11Y-11, A11Y-32, INT-03 |
| `ios-images` | review | `Image\("\|UIImage\(named:` | Asset images. Meaningful ones need a readable label; decorative ones `Image(decorative:)`. | A11Y-14, A11Y-32 |
| `ios-accessibility-modifiers` | inventory | `\.accessibility(Label\|Hint\|AddTraits\|Element\|Value)\(\|accessibilityLabel =` | Accessibility work in the code. Zero hits in a custom UI is a strong signal for A11Y-32. | A11Y-10, A11Y-32 |
| `ios-hardcoded-color` | smell | `Color\(red:\|UIColor\(red:\|#colorLiteral\|Color\(hex:` | Colors outside the asset catalog or theme. They do not adapt to dark mode or increased contrast. | COL-01, COL-12, DS-03 |
| `ios-animations` | inventory | `withAnimation\|\.animation\(\|\.transition\(\|matchedGeometryEffect` | Animations; compare with ios-reduce-motion. | INT-08 |
| `ios-reduce-motion` | inventory | `accessibilityReduceMotion\|isReduceMotionEnabled` | Reduce Motion handling. Zero hits while large or looping animations exist is a finding. | INT-09, A11Y-22 |
| `ios-safe-area` | review | `\.ignoresSafeArea\|\.edgesIgnoringSafeArea` | Content extended under the notch and home indicator. Fine for backgrounds; a defect for text and controls. | RESP-10 |
| `ios-states` | inventory | `ProgressView\(\|ContentUnavailableView\|\.refreshable\|\.redacted\(` | Loading, empty and refresh states. | STATE-01, STATE-04, STATE-02 |

## Android (Jetpack Compose, Views)

Files: `.kt`, `.xml` · detected by any .kt file or an AndroidManifest.xml · sources: [src:androidx-compose-source], [src:material-targets]

- Material 3 components (`Button`, `IconButton`, `Checkbox`…) reserve 48 × 48 dp through `minimumInteractiveComponentSize()`; custom `clickable` elements do not.
- Text sized in `sp` follows the user's font size; `dp` and `px` do not.
- Colors and strings defined in theme files (`Color.kt`, `colors.xml`, `strings.xml`) are expected; probe hits there are not drift.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `android-screens` | inventory | `NavHost\(\|composable\(\|composable<\|ModalBottomSheet\(\|AlertDialog\(\|: (AppCompat\|Component)?Activity\(` | Screens and overlays for the surface map. | — |
| `android-text-size-dp` | smell | `\.dp\.toSp\(\)\|textSize="[0-9.]+(dp\|px)"` | Text sized so that it ignores the user's font size. | TYP-10, A11Y-32, RESP-13 |
| `android-clickable` | review | `\.clickable\s*\{\|\.clickable\(\s*onClick\s*=` | A custom clickable without `role` or `onClickLabel`. TalkBack announces no role; prefer a Material component or pass `role = Role.Button`. Check its size too. | A11Y-11, INT-03, RESP-07 |
| `android-null-description` | review | `contentDescription\s*=\s*null\|android:contentDescription="@null"` | An image or icon hidden from TalkBack. Right for decoration; a defect on an actionable icon. | A11Y-14, A11Y-10 |
| `android-small-size` | review | `\.(size\|height\|width)\(([0-9]\|[1-3][0-9]\|4[0-7])\.dp\)` | A size under 48 dp. Only matters on a custom tappable element; icons inside Material buttons are fine. | RESP-07, A11Y-20, LAY-12 |
| `android-hardcoded-string` | smell | `Text\(\s*(text\s*=\s*)?"[A-Za-z]\|android:text="[A-Za-z]` | User-facing text not in `strings.xml`. | I18N-01 |
| `android-hardcoded-color` | smell | `Color\(0x[0-9A-Fa-f]{6,8}\)\|android:(textColor\|background)="#` | Colors outside the theme (`Color.kt`, `colors.xml`). They bypass dark theme and dynamic color. | COL-01, COL-12, DS-03 |
| `android-insets` | inventory | `enableEdgeToEdge\(\|WindowInsets\|windowInsetsPadding\|safeDrawing\|imePadding` | Edge-to-edge and keyboard insets. Zero hits on a recent target SDK means content may sit under system bars. | RESP-13, RESP-10, RESP-09 |
| `android-back` | inventory | `BackHandler\(\|PredictiveBackHandler\(\|OnBackPressedCallback` | Custom back handling; check that system back still goes back and never loses work silently. | RESP-13, STATE-16 |
| `android-states` | inventory | `CircularProgressIndicator\|LinearProgressIndicator\|PullToRefresh\|LoadState\.` | Loading and refresh states. | STATE-01, STATE-04 |

## Flutter

Files: `.dart` · detected by a pubspec.yaml · sources: [src:flutter-source]

- `IconButton.tooltip` is also its accessible label: an icon button without one is unnamed for screen readers.
- `kMinInteractiveDimension` is 48 logical pixels; Material buttons meet it, `GestureDetector` and `InkWell` children do not by default.
- `textScaleFactor` is deprecated in favour of `TextScaler`; both appear in older code.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `flutter-screens` | inventory | `GoRoute\(\|MaterialPageRoute\|CupertinoPageRoute\|Navigator\.(of\(context\)\.)?push\|showModalBottomSheet\|showDialog` | Screens and overlays for the surface map. | — |
| `flutter-text-scaling-off` | smell | `TextScaler\.noScaling\|TextScaler\.linear\(1(\.0)?\)\|textScaleFactor:\s*1(\.0)?\b` | Text scaling turned off, often app-wide in a `MediaQuery` override. | TYP-10, A11Y-32 |
| `flutter-text-scaling-clamp` | review | `\.clamp\(\s*(minScaleFactor\|maxScaleFactor)` | A cap on text scaling. A low maximum (under about 2) on body text is a defect. | TYP-10, A11Y-32 |
| `flutter-gesture` | review | `GestureDetector\(\|InkWell\(` | A custom tap target. It needs `Semantics(button: true, label: …)` or a button widget, and 48 × 48. | A11Y-11, INT-03, RESP-07 |
| `flutter-icon-button` | review | `IconButton\(` | Icon buttons; each needs `tooltip:`, which is also its accessible label. | A11Y-10 |
| `flutter-images` | review | `Image\.(asset\|network\|file\|memory)\(\|SvgPicture\.` | Images; each needs `semanticLabel:` or `excludeFromSemantics: true`. | A11Y-14 |
| `flutter-hardcoded-string` | smell | `Text\(\s*['"][A-Za-z]` | User-facing text not in the localization files (ARB). | I18N-01 |
| `flutter-hardcoded-color` | smell | `Color\(0x[0-9A-Fa-f]{8}\)\|Color\.fromARGB\(\|Color\.fromRGBO\(` | Colors outside `ThemeData`. They bypass dark mode and the color scheme. | COL-01, COL-12, DS-03 |
| `flutter-reduce-motion` | inventory | `disableAnimationsOf\|\.disableAnimations\|accessibleNavigationOf` | Reduce Motion handling. Zero hits while custom animations exist is a finding. | INT-09, A11Y-22 |
| `flutter-insets` | inventory | `SafeArea\(\|viewPaddingOf\|paddingOf\|viewInsetsOf\|MediaQuery\.of\(context\)\.(padding\|viewPadding\|viewInsets)` | Safe areas and keyboard insets. | RESP-10, RESP-09 |
| `flutter-states` | inventory | `CircularProgressIndicator\|FutureBuilder\|StreamBuilder\|ConnectionState\.\|RefreshIndicator` | Loading, error and refresh states; check each builder handles `hasError`. | STATE-01, STATE-04, STATE-07 |

## React Native (and Expo)

Files: `.tsx`, `.jsx`, `.ts`, `.js` · detected by a package.json that depends on react-native or expo · sources: [src:react-native-docs]

- `allowFontScaling` defaults to `true` on `Text`; turning it off, globally (`Text.defaultProps`) or per element, ignores the user's text size.
- `role` (or the older `accessibilityRole`) and `accessibilityLabel` are not set by `Pressable` and the `Touchable*` components; add them when the content is not plain text.
- Web probes (`references/codebase-recon.md` §3 to §6) still apply to style objects and copy.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `rn-screens` | inventory | `create(NativeStack\|Stack\|BottomTab\|Drawer)Navigator\|<(Stack\|Tabs\|Drawer)\.Screen\|<Modal\b` | Screens and overlays for the surface map. With expo-router, the files under `app/` are the routes. | — |
| `rn-font-scaling-off` | smell | `allowFontScaling(=\{\|\s*[:=]\s*)false\|maxFontSizeMultiplier=\{1(\.0)?\}` | Text that ignores the user's text size, per element or globally. | TYP-10, A11Y-32 |
| `rn-pressables` | review | `<(Pressable\|TouchableOpacity\|TouchableHighlight\|TouchableWithoutFeedback)\b` | Tap targets. Each needs `role` (or `accessibilityRole`), a label when the content is not text, and 44–48 points or `hitSlop`. | A11Y-11, A11Y-10, RESP-07 |
| `rn-images` | review | `<(Image\|ImageBackground\|FastImage)\b` | Images; meaningful ones need `alt` or `accessibilityLabel`. | A11Y-14 |
| `rn-hidden-from-accessibility` | review | `importantForAccessibility="no-hide-descendants"\|accessibilityElementsHidden\|accessible=\{false\}` | Content hidden from screen readers. Check nothing meaningful or actionable is hidden. | A11Y-11, A11Y-32 |
| `rn-hardcoded-string` | smell | `<Text[^>]*>\s*[A-Za-z][^<{]*</Text>` | User-facing text not in the message catalog. | I18N-01 |
| `rn-reduce-motion` | inventory | `isReduceMotionEnabled\|reduceMotionChanged\|useReducedMotion\|ReduceMotion\.` | Reduce Motion handling. Zero hits while custom animations exist is a finding. | INT-09, A11Y-22 |
| `rn-insets` | inventory | `SafeAreaView\|useSafeAreaInsets\|SafeAreaProvider\|KeyboardAvoidingView\|keyboardShouldPersistTaps\|KeyboardAwareScrollView` | Safe areas and keyboard handling. | RESP-10, RESP-09 |
| `rn-states` | inventory | `ActivityIndicator\|RefreshControl\|isLoading\|isPending\|ListEmptyComponent` | Loading, refresh and empty states. | STATE-01, STATE-04, STATE-02 |
