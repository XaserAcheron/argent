module.exports = function (grunt) {
	'use strict';
	
	require('load-grunt-tasks')(grunt, {
		pattern: ['grunt-*']
	});
	
	var config = {
		name: 'xa-argen',
		dir: {
			src: 'src',
			dest: 'dist',
			gdcc: 'gdcc',
		},
		scripts: [
			'argent.acs'
		],
		pkg: require('./package.json')
	};
	
	grunt.initConfig({
		conf: config,

		shell: {
			compile: {
				command: config.scripts.map(function(script) {
					return [
						'"./<%= conf.dir.gdcc %>/gdcc-acc"',
						'--lib-path <%= conf.dir.gdcc %>/lib',
						'./<%= conf.dir.src %>/scripts/' + script,
						'--output ./<%= conf.dir.src %>/acs/' + script.replace('.acs', '.o')
					].join(' ');
				}).join('&&')
			}
		},
		compress: {
			main: {
				options: {
					mode: 'zip',
					archive: './<%= conf.dir.dest %>/<%= conf.name %>.pk3'
				},
				files: [
					{expand: true, cwd: '<%= conf.dir.src %>/', src: ['**'], dest: '/'}
				]
			}
		},
		copy: {
			main: {
				src: '<%= conf.dir.src %>/wadinfo.txt',
				dest: './<%= conf.dir.dest %>/<%= conf.name %>.txt'
			},
			dist: {
				expand: true,
				dot: true,
				cwd: '<%= conf.dir.dest %>',
				dest: '<%= conf.dir.dest %>/',
				src: '<%= conf.name %>.*',
				rename: function(dest, src) {
					return dest + src.replace(/(\.[\w\d_-]+)$/i, '_<%= conf.pkg.version %>$1');
				}
			}
		}
	});
	
	// task aliases
	grunt.registerTask('build', ['shell:compile', 'compress', 'copy:main']);
	grunt.registerTask('dist', ['shell:compile', 'compress', 'copy:main', 'copy:dist']);
	grunt.registerTask('default', ['build']);
};
