webpackHotUpdate("static/development/pages/index.js",{

/***/ "./layouts/Docs.js":
/*!*************************!*\
  !*** ./layouts/Docs.js ***!
  \*************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _components_Boot__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../components/Boot */ "./components/Boot.js");
/* harmony import */ var _components_Navbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/Navbar */ "./components/Navbar.js");
/* harmony import */ var _components_SideNav__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../components/SideNav */ "./components/SideNav.js");
/* harmony import */ var _components_Footer__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../components/Footer */ "./components/Footer.js");
/* harmony import */ var _components_SearchResults__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/SearchResults */ "./components/SearchResults.js");
/* harmony import */ var _components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../components/EjrbussMarkdown */ "./components/EjrbussMarkdown.js");
/* harmony import */ var _components_Places__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../components/Places */ "./components/Places.js");
/* harmony import */ var _components_Logo__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../components/Logo */ "./components/Logo.js");
/* harmony import */ var _components_Timeline__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../components/Timeline */ "./components/Timeline.js");
/* harmony import */ var _components_Bibliography__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../components/Bibliography */ "./components/Bibliography.js");
/* harmony import */ var _lib_Pages__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../lib/Pages */ "./lib/Pages.js");
/* harmony import */ var _Vars__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../Vars */ "./Vars.js");
/* harmony import */ var _Vars__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_Vars__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lib_hooks__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../lib/hooks */ "./lib/hooks.js");
var _jsxFileName = "/Users/ejrbuss/GitHub/chip-gr8/docsource/layouts/Docs.js";


function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

// Components










 // Libraries




/* harmony default export */ __webpack_exports__["default"] = (function (_ref) {
  var pageName = _ref.pageName;
  Object(react__WEBPACK_IMPORTED_MODULE_0__["useEffect"])(function () {
    if (!location.href.endsWith('index/')) {
      location.href = '/index/';
    }
  });
  var page = _lib_Pages__WEBPACK_IMPORTED_MODULE_11__["default"][pageName];
  var searchCtx = Object(_lib_hooks__WEBPACK_IMPORTED_MODULE_13__["useSearch"])();
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react__WEBPACK_IMPORTED_MODULE_0___default.a.Fragment, null, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    id: "page",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 30
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Boot__WEBPACK_IMPORTED_MODULE_1__["default"], _extends({}, page, {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 31
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Navbar__WEBPACK_IMPORTED_MODULE_2__["default"], {
    searchCtx: searchCtx,
    showScrollMarker: true,
    showSearch: true,
    leftLinks: react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Places__WEBPACK_IMPORTED_MODULE_7__["default"], {
      home: true,
      __source: {
        fileName: _jsxFileName,
        lineNumber: 36
      },
      __self: this
    }),
    rightLinks: react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
      href: _Vars__WEBPACK_IMPORTED_MODULE_12___default.a.github,
      className: "p-md subtle-accent",
      __source: {
        fileName: _jsxFileName,
        lineNumber: 37
      },
      __self: this
    }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
      className: "fab fa-github fa-lg",
      __source: {
        fileName: _jsxFileName,
        lineNumber: 38
      },
      __self: this
    })),
    __source: {
      fileName: _jsxFileName,
      lineNumber: 32
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_SideNav__WEBPACK_IMPORTED_MODULE_3__["default"], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 41
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_SearchResults__WEBPACK_IMPORTED_MODULE_5__["default"], {
    searchCtx: searchCtx,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 42
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    className: "content container grid-md docs",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 43
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Logo__WEBPACK_IMPORTED_MODULE_8__["default"], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 44
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("p", {
    className: "text-center subtext p-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 45
    },
    __self: this
  }, page.version), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    className: "text-center clr-accent subtitle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 46
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: page.subtitle,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 47
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: page.content,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 49
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Timeline__WEBPACK_IMPORTED_MODULE_9__["default"], {
    timeline: page.timeline,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 50
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Bibliography__WEBPACK_IMPORTED_MODULE_10__["default"], {
    content: page.bibliography,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 51
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Footer__WEBPACK_IMPORTED_MODULE_4__["default"], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 54
    },
    __self: this
  }));
});

/***/ })

})
//# sourceMappingURL=index.js.7691df80a21d070a0225.hot-update.js.map