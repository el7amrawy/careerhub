/*!
 * valuenator
 * https://github.com/aadelm/valuenator
 * license: MIT
 */

(function (global) {

    "use strict";

    var module = {
        id: "valuenator",
        version: "1.0.1"
    };

    if (typeof exports === "object") {
        module.exports = module;
    } else if (typeof define === "function" && define.amd) {
        define(module);
    } else {
        global.valuenator = module;
    }

    module.create = function (options) {

        var opts = options || {};

        // defaults
        opts.min = opts.min || 0;
        opts.max = opts.max || 100;
        opts.step = opts.step || 1;
        opts.value = opts.value || opts.min;
        opts.formatter = opts.formatter || function (v) {
            return v;
        };
        opts.onValueChanged = opts.onValueChanged || function () {
        };

        var value = opts.value;

        var setValue = function (newValue) {
            if (newValue < opts.min) {
                newValue = opts.min;
            } else if (newValue > opts.max) {
                newValue = opts.max;
            }

            if (newValue !== value) {
                value = newValue;
                opts.onValueChanged(value);
            }
        };

        return {
            getValue: function () {
                return value;
            },
            setValue: setValue,
            increment: function () {
                setValue(value + opts.step);
            },
            decrement: function () {
                setValue(value - opts.step);
            }
        };

    };

})(this); 