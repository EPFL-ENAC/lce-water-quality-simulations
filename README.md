# it4r-webmap

## Configuration

Two external json files to load configuration in [`.env`](.env) :

- **VITE_PARAMETERS_URL**: Webmap parameters following [this JSON Schema](schema/parameters.schema.json)
- **VITE_STYLE_URL**: [MapLibre style](https://maplibre.org/maplibre-style/)

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
   1. Run `Extensions: Show Built-in Extensions` from VSCode's command palette
   2. Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
## exploration:

Gdal netcdf - https://gdal.org/drivers/raster/netcdf.html
gdal2tiles

maptiler-server https://maptiler-tileserver.readthedocs.io/en/latest/

for generatique the doc

https://github.com/maptiler/tileserver-gl

https://www.maptiler.com

https://github.com/christophenoel/geozarr-spec
https://github.com/spacebel/geozarr-openlayers

https://mygeodata.cloud/converter/netcdf-to-tif


# for database / backend

zod github validation
koskimas/kysely github

drizzle orm typescript
nexxel.dev


kysely vs drizzle ?

Use https://vee-validate.logaretm.com/v4/integrations/zod-schema-validation/

for validation...