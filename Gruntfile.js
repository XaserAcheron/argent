module.exports = function (grunt) {
	'use strict';
	
	require('load-grunt-tasks')(grunt, {
		pattern: ['grunt-*']
	});
	
	var config = {
		name: 'xa-argen',
		src: 'src',
		pkg: require('./package.json')
	};
	
	grunt.initConfig({
		conf: config,

		compress: {
			main: {
				options: {
					mode: 'zip',
					archive: './dist/<%= conf.name %>.pk3'
				},
				files: [
					{expand: true, cwd: 'src/', src: ['**'], dest: '/'}
				]
			}
		},
		copy: {
			main: {
				src: 'src/wadinfo.txt',
				dest: './dist/<%= conf.name %>.txt'
			},
			dist: {
				expand: true,
				dot: true,
				cwd: 'dist',
				dest: 'dist/',
				src: '<%= conf.name %>.*',
				rename: function(dest, src) {
					return dest + src.replace(/(\.[\w\d_-]+)$/i, '_<%= conf.pkg.version %>$1');
				}
			}
		}
	});
	
	// task aliases
	grunt.registerTask('build', ['compress', 'copy:main']);
	grunt.registerTask('dist', ['compress', 'copy:main', 'copy:dist']);
	grunt.registerTask('default', ['build']);
};
