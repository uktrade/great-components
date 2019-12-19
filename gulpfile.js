'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const del = require('del');

const PROJECT_DIR = path.resolve(__dirname);
const GREAT_STYLES = `${PROJECT_DIR}/node_modules/great-styles/src`;

const SASS_FILES = `${PROJECT_DIR}/demo/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/demo/static/styles`;
const CSS_FILES = `${PROJECT_DIR}/demo/static/styles/**/*.css`;
const CSS_MAPS = `${PROJECT_DIR}/demo/static/styles/**/*.css.map`;
const IMAGES_SRC = `${GREAT_STYLES}/images/**/*`;
const IMAGES_DEST = `${PROJECT_DIR}/demo/static/vendor/images`;


gulp.task('clean:styles', function() {
  return del([CSS_FILES, CSS_MAPS])
});

gulp.task('clean:images', function() {
  return del([IMAGES_DEST])
});

gulp.task('sass:compile', function () {
  return gulp.src(SASS_FILES)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        GREAT_STYLES,
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(CSS_DIR));
});

gulp.task('images', function () {
  return gulp.src(IMAGES_SRC)
  .pipe(gulp.dest(IMAGES_DEST));
});

gulp.task('watch', function () {
  gulp.watch(
    [SASS_FILES],
    gulp.series('sass:compile')
  );
});

gulp.task('clean', gulp.series('clean:styles', 'clean:images'));

gulp.task('styles', gulp.series('clean:styles', 'sass:compile'));

gulp.task('build', gulp.series('clean:images', 'images', 'styles'));

gulp.task('default', gulp.series('clean', 'images', 'styles', 'watch'));
