webpackHotUpdate("static/development/pages/about.js",{

/***/ "./layouts/About.js":
/*!**************************!*\
  !*** ./layouts/About.js ***!
  \**************************/
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
/* harmony import */ var _components_Profile__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../components/Profile */ "./components/Profile.js");
/* harmony import */ var _lib_Pages__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../lib/Pages */ "./lib/Pages.js");
/* harmony import */ var _Vars__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../Vars */ "./Vars.js");
/* harmony import */ var _Vars__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_Vars__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lib_hooks__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../lib/hooks */ "./lib/hooks.js");
var _jsxFileName = "/Users/Andrew/GitHub/chip-gr8/docsource/layouts/About.js";


function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

// Components







 // Libraries




/* harmony default export */ __webpack_exports__["default"] = (function (_ref) {
  var pageName = _ref.pageName;
  var page = _lib_Pages__WEBPACK_IMPORTED_MODULE_9__["default"][pageName];
  var searchCtx = Object(_lib_hooks__WEBPACK_IMPORTED_MODULE_11__["useSearch"])();
  return react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react__WEBPACK_IMPORTED_MODULE_0___default.a.Fragment, null, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    id: "page",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 21
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Boot__WEBPACK_IMPORTED_MODULE_1__["default"], _extends({}, page, {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 22
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Navbar__WEBPACK_IMPORTED_MODULE_2__["default"], {
    searchCtx: searchCtx,
    showScrollMarker: true,
    showSearch: true,
    leftLinks: react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Places__WEBPACK_IMPORTED_MODULE_7__["default"], _extends({}, _defineProperty({}, page.place, true), {
      __source: {
        fileName: _jsxFileName,
        lineNumber: 27
      },
      __self: this
    })),
    rightLinks: react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
      target: "_blank",
      href: _Vars__WEBPACK_IMPORTED_MODULE_10___default.a.github,
      className: "p-md subtle-accent",
      __source: {
        fileName: _jsxFileName,
        lineNumber: 28
      },
      __self: this
    }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
      className: "fab fa-github fa-lg",
      __source: {
        fileName: _jsxFileName,
        lineNumber: 29
      },
      __self: this
    })),
    __source: {
      fileName: _jsxFileName,
      lineNumber: 23
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_SideNav__WEBPACK_IMPORTED_MODULE_3__["default"], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 32
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_SearchResults__WEBPACK_IMPORTED_MODULE_5__["default"], {
    searchCtx: searchCtx,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 33
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", {
    className: "content container grid-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 34
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\n# Meet Our Team\n\nWe are a group of Software and Electrical Engineering students from the University of Victoria. We combined our passions for programming, artificial intelligence, and gaming to deliver an artificial intelligence tool to help newcomers discover a love for technology and creating something new.\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 35
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/Eric.png",
    name: "Eric Buss",
    position: "Team Lead / Developer",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 42
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nEric is a fourth-year Software Engineering student graduating in August 2019. He is a Canadian through-and-through having already lived and worked in 5 Canadian provinces. His love for creative projects and problem-solving led him to his studies at UVic. Eric brings his passion for code and design to all his projects both in and out of school.",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 43
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://www.linkedin.com/in/ejrbuss/",
    className: "subtle mr-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 48
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-linkedin",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 48
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://github.com/ejrbuss",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 49
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 49
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/Torrey.png",
    right: true,
    name: "Torrey Randolph",
    position: "Low Level Architect",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 51
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nTorrey plans to graduate from UVic with a Bachelor of Software Engineering in 2019. Come October, she will be starting her career as a Firmware Developer at Reliable Controls in the beautiful city of Victoria. She hopes to one day follow her dream of working for NASA.",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 52
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://www.linkedin.com/in/torrey-randolph/",
    className: "subtle mr-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 57
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-linkedin",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 57
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://github.com/torreyr",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 58
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 58
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/Jon.png",
    name: "Jonathan Bezeau",
    position: "Artist / Developer",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 60
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nJon is a fourth year Software Engineering student aiming to graduate in 2020. He hails from Prince George BC, and moved to Victoria to study general engineering at UVic in 2014. Jon spends his time writing Dungeons and Dragons campaigns and working on his personal coding projects. After graduation he hopes to remain in Victoria.",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 61
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://github.com/UltravioletVoodoo",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 67
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 67
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/James.png",
    right: true,
    name: "James Barlow",
    position: "UI Developer",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 69
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nJames is graduating from UVic with a Software Engineering degree and Business minor in August 2019. He wants to try his hand at running a business someday, but until then he hopes to work on technologies that help people. Further education is still a possibility for the future, but right now he is excited to start his career.\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 70
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://github.com/jbarlo",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 77
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 77
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/Andrew.png",
    name: "Andrew Wiggins",
    position: "Web Developer",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 79
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nAndrew is a fourth year Software Engineering student who plans on graduating in April 2020. He started his University career in the Faculty of Science, but transitioned into Software Engineering after discovering a fondness for programming. After graduation he plans on moving to Vancouver to pursue a career as a developer.\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 80
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://www.linkedin.com/in/awiggs96/",
    className: "subtle mr-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 86
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-linkedin",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 86
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://www.github.com/awiggs",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 87
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 87
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/John.png",
    right: true,
    name: "Forrest Curry",
    position: "AI Developer",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 89
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nForrest is a fourth year Bachelor of Electrical Engineering student with a Minor in Computer Science. He has experience working both high level technologies such as web development and low level technologies such as integrated circuit design as well as software designed to target embedded systems. As for computer support, he has worked as an IT profession for both desktop and remote system administration. Personally, he loves a good sci-fi book and has been playing guitar since he was 17.",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 90
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://www.linkedin.com/in/john-curry/",
    className: "subtle mr-md",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 95
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-linkedin",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 95
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
    href: "https://github.com/john-curry",
    className: "subtle",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 96
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("i", {
    className: "fab fa-github",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 96
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("br", {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 98
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\n# Acknowledgements\nChip-Gr8 would not have been possible without the help of several individuals. We would like to acknowledge their involvement in Chip-Gr8's development journey, and extend to them our deepest thanks.\n\n## Faculty Supervisor\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 99
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Profile__WEBPACK_IMPORTED_MODULE_8__["default"], {
    src: "../static/img/RichLittle.jpg",
    name: "Rich Little",
    position: "Faculty Supervisor",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 107
    },
    __self: this
  }, react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\nWe chose Rich Little as our faculty supervisor for his background in algorithms and based on our positive experiences with him in CSC 225 and 226 courses. He was responsible for supervising the project during its development cycle and for marking all of the milestones. Thank you to Rich Little for the help he provided along the way.\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 108
    },
    __self: this
  })), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("br", {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 115
    },
    __self: this
  }), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_EjrbussMarkdown__WEBPACK_IMPORTED_MODULE_6__["default"], {
    source: "\n## Supporters\n\nThank you to Dr. Xiaodai Dong for being the primary instructor this semester.\n\nThank you to Dr. Ilamparithi for being the course coordinator this semester.\n\nThank you to Sai Prakash Reddy Konda, our TA, for their help with the course.\n",
    __source: {
      fileName: _jsxFileName,
      lineNumber: 116
    },
    __self: this
  }))), react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_Footer__WEBPACK_IMPORTED_MODULE_4__["default"], {
    __source: {
      fileName: _jsxFileName,
      lineNumber: 129
    },
    __self: this
  }));
});

/***/ })

})
//# sourceMappingURL=about.js.d376c4f6d1869c6661f5.hot-update.js.map