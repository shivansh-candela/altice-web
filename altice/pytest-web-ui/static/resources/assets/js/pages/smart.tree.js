/* Smart UI v13.1.0 (2022-Mar) 
Copyright (c) 2011-2022 jQWidgets. 
License: https://htmlelements.com/license/ */


/******/
(() => { // webpackBootstrap
    /******/
    var __webpack_modules__ = ({

        /***/
        2612:
        /***/
            (() => {

            Smart("smart-button", class extends Smart.ContentElement {
                static get properties() { return { value: { type: "string" }, name: { type: "string" }, type: { value: "button", type: "string" }, clickMode: { allowedValues: ["hover", "press", "release", "pressAndRelease"], type: "string", value: "release" } } }
                static get styleUrls() { return ["smart.button.css"] }
                template() { return "<button class=\"smart-button smart-unselectable\" inner-h-t-m-l='[[innerHTML]]' id='button' type='[[type]]' name='[[name]]' value='[[value]]' disabled='[[disabled]]' role=\"presentation\"></button>" }
                refresh() {}
                static get listeners() { return { "button.down": "_downHandler", "button.mouseenter": "_mouseEnterHandler", "button.mouseleave": "_mouseLeaveHandler", "button.touchend": "_touchEndHandler", "button.click": "_clickHandler", "button.up": "_upHandler", up: "_upHandler", "button.focus": "_focusHandler", "button.blur": "_blurHandler" } }
                focus() {
                    const e = this;
                    e.$.button ? e.$.button.focus() : HTMLElement.prototype.focus.call(e)
                }
                blur() {
                    const e = this;
                    e.$.button ? e.$.button.blur() : HTMLElement.prototype.blur.call(e)
                }
                _upHandler(e) {
                    const t = this;
                    if (e.stopPropagation(), t.$.setAttributeValue("active", !1), t.dataset.target) {
                        const n = document.querySelector(t.dataset.target);
                        let a = t.dataset.toggle;
                        const r = "smart-window".toLowerCase();
                        if (n && n.nodeName.toLowerCase() === r && "modal" === a && (a = "openModal"), "tab" === a || "pill" === a || "list" === a) {
                            const e = this.closest(".nav, .list-group"),
                                a = '[data-toggle="tab"], [data-toggle="pill"], [data-toggle="list"]',
                                r = !e || "UL" !== e.nodeName && "OL" !== e.nodeName ? e.children(".active") : e.querySelectorAll("li > .active");
                            if (e) {
                                const n = e.querySelectorAll(a);
                                for (let e = 0; e < n.length; e++) n[e].classList.remove("primary");
                                for (let e = 0; e < r.length; e++) r[e].classList.remove("active");
                                let i = t.parentNode;
                                for (; i;) {
                                    if ("LI" === i.nodeName) { i.classList.add("active"); break }
                                    i = i.parentNode
                                }
                                t.classList.add("primary")
                            }
                            return n.parentNode.querySelectorAll(".active").forEach((e => { e.classList.remove("active"), e.classList.add("smart-hidden") })), n.classList.add("active"), void n.classList.remove("smart-hidden")
                        }
                        a && n && !n[a] && "collapse" === a && (setTimeout((() => { n.classList.contains("smart-hidden") ? n.classList.remove("smart-hidden") : n.classList.add("smart-hidden") })), e.originalEvent.preventDefault()), a && n && !n[a] && "dropdown" === a ? (setTimeout((() => { n.opened = !n.opened })), e.originalEvent.preventDefault()) : a && n && n[a] && (setTimeout((() => { n[a]() }), 50), e.originalEvent.preventDefault())
                    }
                }
                _focusHandler() { this.$.setAttributeValue("focus", !0), this.$.fireEvent("focus") }
                _blurHandler() { this.$.setAttributeValue("focus", !1), this.$.fireEvent("blur") }
                _clickHandler(e) {
                    const t = this;
                    ("release" !== t.clickMode && "pressAndRelease" !== t.clickMode || t.readonly) && (e.preventDefault(), e.stopPropagation())
                }
                _downHandler(e) {
                    const t = this;
                    if (!(t.disabled || (t.hasRippleAnimation && Smart.Utilities.Animation.Ripple.animate(t, e.pageX, e.pageY), t.$.setAttributeValue("active", !0), "press" !== t.clickMode && "pressAndRelease" !== t.clickMode || t.readonly))) {
                        if (t.hasAttribute("smart-blazor")) return void t.$.dispatchEvent(new Event("click"));
                        const n = "buttons" in e ? e.buttons : e.which;
                        t.$.fireEvent("click", { buttons: n, clientX: e.clientX, clientY: e.clientY, pageX: e.pageX, pageY: e.pageY, screenX: e.screenX, screenY: e.screenY })
                    }
                }
                _mouseEnterHandler(e) {
                    const t = this;
                    if (!t.readonly && (t.$button.setAttributeValue("hover", !0), t.$.setAttributeValue("hover", !0), "hover" === t.clickMode)) {
                        const n = "buttons" in e ? e.buttons : e.which;
                        if (t.hasAttribute("smart-blazor")) return void t.$.dispatchEvent(new Event("click"));
                        t.$.fireEvent("click", { buttons: n, clientX: e.clientX, clientY: e.clientY, pageX: e.pageX, pageY: e.pageY, screenX: e.screenX, screenY: e.screenY })
                    }
                }
                _touchEndHandler() {
                    const e = this;
                    setTimeout((function() { e.$button.setAttributeValue("hover", !1), e.$.setAttributeValue("hover", !1) }), 300)
                }
                _mouseLeaveHandler() { this.$button.setAttributeValue("hover", !1), this.$.setAttributeValue("hover", !1) }
                propertyChangedHandler(e, t, n) { super.propertyChangedHandler(e, t, n); const a = this; "disabled" === e ? (a._setFocusable(), a.$button && a.$button.setAttributeValue("hover", !1), a.$.setAttributeValue("hover", !1), a instanceof Smart.RepeatButton && a._stopRepeat()) : "unfocusable" === e && a._setFocusable() }
                _setFocusable() {
                    const e = this,
                        t = e.$.button ? e.$.button : e;
                    if (e.disabled || e.unfocusable) return t.removeAttribute("tabindex"), void(t.tabIndex = -1);
                    t.tabIndex = e.tabIndex > 0 ? e.tabIndex : 0
                }
                ready() {
                    const e = this;
                    super.ready(), e.setAttribute("role", "button"), e._setFocusable(), e.enableShadowDOM && e.$.hiddenInput && e.appendChild(e.$.hiddenInput)
                }
            }), Smart("smart-repeat-button", class extends Smart.Button {
                static get properties() { return { delay: { value: 50, type: "number" }, initialDelay: { value: 150, type: "number" } } }
                static get listeners() { return { "button.down": "_startRepeat", "button.mouseenter": "_overriddenHandler", "button.mouseleave": "_overriddenHandler", "button.pointerenter": "_updateInBoundsFlag", "button.pointerleave": "_updateInBoundsFlag", "button.touchmove": "_touchmoveHandler", "document.up": "_stopRepeat" } }
                _clickHandler(e) {
                    const t = this;
                    ("release" !== t.clickMode || t.preventDefaultClick || t.readonly || t.disabled) && (e.preventDefault(), e.stopPropagation(), t.preventDefaultClick = !1)
                }
                _updateInBoundsFlag(e) { const t = this; - 1 !== e.type.indexOf("leave") ? (t._isPointerInBounds = !1, t.$button.setAttributeValue("hover", !1), t.$.setAttributeValue("hover", !1)) : (t._isPointerInBounds = !0, t.$button.setAttributeValue("hover", !0), t.$.setAttributeValue("hover", !0)), 1 !== ("buttons" in e ? e.buttons : e.which) && t._stopRepeat(e) }
                _startRepeat(e) {
                    const t = this;
                    t.setAttribute("active", ""), t._initialTimer || t.readonly || (t._initialTimer = setTimeout((function() {
                        t._repeatTimer = setInterval((() => {
                            if (t._isPointerInBounds) {
                                if (t.hasAttribute("smart-blazor")) return t.$.dispatchEvent(new Event("click")), void(t.preventDefaultClick = !0);
                                const n = "buttons" in e ? e.buttons : e.which;
                                t.$.fireEvent("click", { buttons: n, clientX: e.clientX, clientY: e.clientY, pageX: e.pageX, pageY: e.pageY, screenX: e.screenX, screenY: e.screenY }), t.preventDefaultClick = !0
                            }
                        }), t.delay)
                    }), t.initialDelay))
                }
                _stopRepeat(e) {
                    const t = this;
                    t.readonly || e && ("pointercancel" === e.type || e.originalEvent && "pointercancel" === e.originalEvent.type) || (t.$.setAttributeValue("active", !1), t._repeatTimer && (clearInterval(t._repeatTimer), t._repeatTimer = null), t._initialTimer && (clearTimeout(t._initialTimer), t._initialTimer = null))
                }
                _touchmoveHandler(e) { this.preventDefaultClick && e.cancelable && (e.preventDefault(), e.stopPropagation()) }
                _overriddenHandler() {}
            }), Smart("smart-toggle-button", class extends Smart.Button {
                static get properties() { return { checked: { value: !1, type: "boolean?" }, falseContent: { value: "", reflectToAttribute: !1, type: "string" }, indeterminateContent: { value: "", reflectToAttribute: !1, type: "string" }, indeterminate: { value: !1, type: "boolean" }, trueContent: { value: "", reflectToAttribute: !1, type: "string" }, indeterminateTemplate: { value: null, type: "any" }, trueTemplate: { value: null, type: "any" }, falseTemplate: { value: null, type: "any" }, type: { value: "toggle", type: "string", defaultReflectToAttribute: !0, readonly: !0 } } }
                static get listeners() { return { keydown: "_keyHandler", keyup: "_keyHandler", dragstart: "_dragStartHandler", "button.click": "_buttonClickHandler", "button.mouseenter": "_buttonMouseEnterHandler", "button.mouseleave": "_buttonMouseLeaveHandler", "document.up": "_documentUpHandler" } }
                ready() { super.ready(), this._setAriaState() }
                _setAriaState() {
                    const e = this,
                        t = e.checked;
                    null !== t ? e.setAttribute("aria-pressed", t) : e.setAttribute("aria-pressed", "mixed")
                }
                _buttonClickHandler() {}
                _buttonMouseLeaveHandler() { this.removeAttribute("hover") }
                _buttonMouseEnterHandler() {
                    const e = this;
                    e.setAttribute("hover", ""), e.disabled || e.readonly || "hover" !== e.clickMode || (e._changeCheckState("pointer"), e.focus(), e._updateHidenInputNameAndValue())
                }
                _documentUpHandler(e) {
                    const t = this;
                    t._pressed && (t._pressed = !1, t.disabled || t.readonly || "press" === t.clickMode || "pointercancel" === e.originalEvent.type || (t._changeCheckState("pointer"), t.focus(), t._updateHidenInputNameAndValue()))
                }
                _downHandler(e) {
                    const t = this;
                    t.disabled || t.readonly || (t.hasRippleAnimation && Smart.Utilities.Animation.Ripple.animate(t, e.pageX, e.pageY), t._pressed = !0, "press" !== t.clickMode && "pressAndRelease" !== t.clickMode || (t._changeCheckState("pointer"), t.hasAttribute("smart-blazor") ? t.$.dispatchEvent(new Event("click")) : t.$.fireEvent("click"), t._updateHidenInputNameAndValue()), "press" === t.clickMode && (e.preventDefault(), e.stopPropagation()))
                }
                _dragStartHandler(e) { e.preventDefault() }
                _keyHandler(e) {
                    const t = this;
                    if (!0 !== t.disabled && !t.readonly && 32 === e.keyCode) {
                        if ("keydown" === e.type) return void e.preventDefault();
                        if ("none" === t.switchMode) return;
                        t._changeCheckState("keyboard"), t._updateHidenInputNameAndValue()
                    }
                }
                _changeCheckState(e) {
                    const t = this;
                    let n = null;
                    null === t.checked ? t.checked = !0 : (n = t.checked, t.checked = !t.checked), t._handleTextSelection(), t.$.fireEvent("change", { value: t.checked, oldValue: n, changeType: e }), t.checked ? t.$.fireEvent("checkValue", { changeType: e }) : t.$.fireEvent("uncheckValue", { changeType: e }), t._setAriaState()
                }
                _handleTextSelection() {
                    const e = this;
                    e.$.addClass("smart-unselectable"), e.timer && clearTimeout(e.timer), e.timer = setTimeout((() => e.$.removeClass("smart-unselectable")), 500)
                }
                propertyChangedHandler(e, t, n) {
                    super.propertyChangedHandler(e, t, n);
                    const a = this;
                    if ("checked" === e) return a.$.fireEvent("change", { value: n, oldValue: t, changeType: "api" }), void a._setAriaState();
                    switch (e) {
                        case "trueTemplate":
                            a._handleTemplate(!0);
                            break;
                        case "falseTemplate":
                            a._handleTemplate(!1);
                            break;
                        case "indeterminateTemplate":
                            a._handleTemplate()
                    }
                }
                _htmlBindOnInitialization() {
                    const e = this;
                    e._bindContentProperty("trueContent", "smart-true-content"), e._bindContentProperty("falseContent", "smart-false-content"), e._bindContentProperty("indeterminateContent", "smart-indeterminate-content")
                }
                _bindContentProperty(e, t) {
                    const n = this;
                    if (!n.$[e + "Container"]) return;
                    let a = document.createElement("div");
                    a.innerHTML = n.innerHTML;
                    let r, i = a.getElementsByClassName(t);
                    if (i.length > 0)
                        for (let e = 0; e < i.length; e++) r = i[e];
                    "" === n[e] && (n[e] = void 0 === r ? "" : r.outerHTML), n.$[e + "Container"].innerHTML = n[e]
                }
                _updateContentProperties() {
                    const e = this;

                    function t(t) { e.$[t + "Container"] && (e[t] = e.$[t + "Container"].innerHTML) }
                    t("trueContent"), t("falseContent"), t("indeterminateContent")
                }
                _updateHidenInputValue() {
                    const e = this;
                    if (!e.$.hiddenInput) return;
                    let t;
                    t = null === e.checked ? "null" : !1 === e.checked ? "off" : e.value || "on", e.$.hiddenInput.setAttribute("value", t)
                }
                _updateHidenInputName() {
                    const e = this;
                    if (!e.$.hiddenInput) return;
                    let t = !1 === e.checked ? "" : e.name || "";
                    e.$.hiddenInput.setAttribute("name", t)
                }
                _updateHidenInputNameAndValue() { this._updateHidenInputName(), this._updateHidenInputValue() }
                _handleTemplate(e, t) {
                    const n = this;
                    let a, r, i;
                    if (!0 === e ? (a = n.trueTemplate, r = n.$.trueContentContainer, i = n.trueContent) : !1 === e ? (a = n.falseTemplate, r = n.$.falseContentContainer, i = n.falseContent) : (a = n.indeterminateTemplate, r = n.$.indeterminateContentContainer, i = n.indeterminateContent), t && (r.innerHTML = i || ""), null === a || !a) return;
                    if ("function" == typeof a) return void a(r, { value: i });
                    if (!("content" in document.createElement("template"))) return void n.error(n.localize("htmlTemplateNotSuported", { elementType: n.nodeName.toLowerCase() }));
                    if (a = document.getElementById(a), null === a || !("content" in a)) return void n.error(n.localize("invalidTemplate", { elementType: n.nodeName.toLowerCase(), property: "template" }));
                    const l = a.content,
                        o = l.childNodes.length,
                        s = /{{\w+}}/g;
                    let u, d = [];
                    for (let e = 0; e < o; e++)
                        for (u = s.exec(l.childNodes[e].innerHTML); u;) d.push({ childNodeIndex: e, bindingString: u[0] }), u = s.exec(l.childNodes[e].innerHTML);
                    const c = d.length;
                    let p, h, m = document.importNode(a.content, !0);
                    for (let e = 0; e < c; e++) { p = m.childNodes[d[e].childNodeIndex], h = d.length; for (let t = 0; t < h; t++) p.innerHTML = p.innerHTML.replace(d[e].bindingString, i) }
                    r.innerHTML = "";
                    for (let e = 0; e < m.childNodes.length; e++) m.childNodes[e].outerHTML && (r.innerHTML += m.childNodes[e].outerHTML)
                }
            });

            /***/
        }),

        /***/
        9097:
        /***/
            (() => {

            Smart("smart-check-box", class extends Smart.ToggleButton {
                static get properties() { return { checkMode: { value: "both", allowedValues: ["both", "input", "label"], type: "string" }, type: { value: "checkbox", type: "string", defaultReflectToAttribute: !0, readonly: !0 } } }
                template() { return "<div id='container' class='smart-container' role=\"presentation\">\n                    <div class='smart-overlay' role=\"presentation\"></div>\n                    <span id='checkBoxInput' class='smart-input' aria-hidden=\"true\"></span>\n                    <span id='checkBoxLabel' inner-h-t-m-l='[[innerHTML]]' class='smart-label'><content></content></span>\n                    <input id='hiddenInput' class='smart-hidden-input' type='hidden'>\n                </div>" }
                static get listeners() { return { down: "_downHandler", "document.up": "_documentUpHandler", "checkBoxInput.mouseenter": "_mouseEnterHandler", "checkBoxInput.mouseleave": "_mouseLeaveHandler", focus: "_focusHandler", blur: "_blurHandler" } }
                static get styleUrls() { return ["smart.toggle.css"] }
                _focusHandler() { this.$.setAttributeValue("focus", !0) }
                _blurHandler() { this.$.setAttributeValue("focus", !1) }
                _mouseEnterHandler() { this.$.setAttributeValue("hover", !0) }
                _mouseLeaveHandler() { this.$.setAttributeValue("hover", !1) }
                ready() {
                    const e = this;
                    super.ready(), e.setAttribute("role", "checkbox"), e.indeterminate && (e._valueCache = e.checked, e.checked = null, e._setAriaState()), e.classList.add("smart-toggle-box"), e._updateHidenInputNameAndValue()
                }
                propertyChangedHandler(e, t, a) {
                    super.propertyChangedHandler(e, t, a);
                    const n = this;
                    switch (n._updateContentProperties(), e) {
                        case "indeterminate":
                            a ? (n._valueCache = n.checked, n.checked = null) : n.checked = n._valueCache, n._setAriaState(), n._updateHidenInputNameAndValue();
                            break;
                        case "value":
                        case "checked":
                            n._updateHidenInputNameAndValue();
                            break;
                        case "name":
                            n._updateHidenInputName()
                    }
                }
                _documentUpHandler(e) {
                    const t = this;
                    if (!t._pressed || "pointercancel" === e.originalEvent.type) return;
                    const a = t.enableShadowDOM ? e.originalEvent.composedPath()[0] : e.originalEvent.target;
                    if (t._pressed = !1, t.$.setAttributeValue("active", !1), !(t.disabled || t.readonly || "input" === t.checkMode && a !== t.$.checkBoxInput || "label" === t.checkMode && a !== t.$.checkBoxLabel)) {
                        if ("press" === t.clickMode) return e.preventDefault(), void e.stopPropagation();
                        t._changeCheckState("pointer"), t.focus(), t._handleTextSelection(), t._updateHidenInputNameAndValue()
                    }
                }
                _downHandler(e) {
                    const t = this,
                        a = t.enableShadowDOM ? e.originalEvent.composedPath()[0] : e.originalEvent.target;
                    if (!(t.disabled || t.readonly || "input" === t.checkMode && a !== t.$.checkBoxInput || "label" === t.checkMode && a !== t.$.checkBoxLabel)) {
                        if (t.$.setAttributeValue("active", !0), t.hasRippleAnimation) {
                            const e = t.$.checkBoxInput.getBoundingClientRect(),
                                a = window.scrollX || window.pageXOffset,
                                n = window.scrollY || window.pageYOffset;
                            Smart.Utilities.Animation.Ripple.animate(t.$.checkBoxInput, e.left + e.width / 2 + a, e.top + e.height / 2 + n)
                        }
                        t._pressed = !0, "press" !== t.clickMode && "pressAndRelease" !== t.clickMode || (t._changeCheckState("pointer"), t.$.fireEvent("click"), t.focus(), t._updateHidenInputNameAndValue())
                    }
                }
                _setAriaState() {
                    const e = this,
                        t = e.checked;
                    null !== t ? e.setAttribute("aria-checked", t) : e.setAttribute("aria-checked", "mixed")
                }
            });

            /***/
        }),

        /***/
        6321:
        /***/
            (() => {

            ! function() {
                const e = "11.0.0",
                    t = [];
                let n = "Smart";
                if (window[n] && window[n].Version) {
                    if (window[n].Version === e) return;
                    if (window[n].Version !== e) n += e;
                    else { let e = 2; for (; window[n];) n += e.toString(), e++ }
                }
                const r = navigator.userAgent.indexOf("Edge") > -1 && navigator.appVersion.indexOf("Edge") > -1;
                document.elementsFromPoint || (document.elementsFromPoint = document.msElementsFromPoint);
                class o {
                    static isBoolean(e) { return "boolean" == typeof e }
                    static isFunction(e) { return !!(e && e.constructor && e.call && e.apply) }
                    static isArray(e) { return Array.isArray(e) }
                    static isObject(e) { return e && ("object" == typeof e || this.isFunction(e)) || !1 }
                    static isDate(e) { return e instanceof Date }
                    static isString(e) { return "string" == typeof e }
                    static isNumber(e) { return "number" == typeof e }
                    static getType(e) {
                        const t = this,
                            n = ["Boolean", "Number", "String", "Function", "Array", "Date", "Object"].find((n => { if (t["is" + n](e)) return n }));
                        return n ? n.toLowerCase() : void 0
                    }
                }
                class i {
                    static animate(e, t, r, o) {
                        const i = e;
                        if (!i || i instanceof HTMLElement == 0) return;
                        if (0 === i.getElementsByClassName("smart-ripple").length) {
                            const e = document.createElement("span");
                            e.classList.add("smart-ripple"), e.setAttribute("role", "presentation");
                            let t = !0,
                                r = null;
                            if (window[n].EnableShadowDOM && i.enableShadowDOM && !0 !== i.isInShadowDOM) {
                                for (let e = 0; e < i.shadowRoot.host.shadowRoot.children.length; e++) "link" !== i.shadowRoot.host.shadowRoot.children[e].tagName.toLowerCase() && (r = i.shadowRoot.host.shadowRoot.children[e]);
                                i.shadowRoot.host.shadowRoot.querySelector(".smart-ripple") && (t = !1)
                            } else r = i.firstElementChild;
                            t && (r && !r.noRipple && r.offsetHeight > 0 ? r.appendChild(e) : i.appendChild(e))
                        }
                        let s = null;
                        if (s = window[n].EnableShadowDOM && i.shadowRoot ? i.shadowRoot.host.shadowRoot.querySelector(".smart-ripple") : i.getElementsByClassName("smart-ripple")[0], !s) return;
                        s.innerHTML = "", s.classList.remove("smart-animate"), s.style.height = s.style.width = Math.max(i.offsetHeight, i.offsetWidth) + "px";
                        const a = window.getComputedStyle(s.parentElement),
                            l = parseInt(a.borderLeftWidth) || 0,
                            d = parseInt(a.borderTopWidth) || 0,
                            c = i.getBoundingClientRect(),
                            u = t - (c.left + window.pageXOffset) - s.offsetWidth / 2 - l,
                            p = r - (c.top + window.pageYOffset) - s.offsetHeight / 2 - d;
                        s.style.left = u + "px", s.style.top = p + "px", s.classList.add("smart-animate"), s.addEventListener("animationend", (function e() { s.parentElement && s.parentElement.removeChild(s), o && o(), s.removeEventListener("animationend", e), s.removeEventListener("animationcancel", e) })), s.addEventListener("animationcancel", (function e() { s.parentElement && s.parentElement.removeChild(s), o && o(), s.removeEventListener("animationcancel", e), s.removeEventListener("animationend", e) }))
                    }
                }
                class s {
                    static easeInQuad(e, t, n, r) { return n * (e /= r) * e + t }
                    static easeOutQuad(e, t, n, r) { return -n * (e /= r) * (e - 2) + t }
                    static easeInOutQuad(e, t, n, r) { return (e /= r / 2) < 1 ? n / 2 * e * e + t : -n / 2 * (--e * (e - 2) - 1) + t }
                    static easeInCubic(e, t, n, r) { return n * (e /= r) * e * e + t }
                    static easeOutCubic(e, t, n, r) { return n * ((e = e / r - 1) * e * e + 1) + t }
                    static easeInOutCubic(e, t, n, r) { return (e /= r / 2) < 1 ? n / 2 * e * e * e + t : n / 2 * ((e -= 2) * e * e + 2) + t }
                    static easeInQuart(e, t, n, r) { return n * (e /= r) * e * e * e + t }
                    static easeOutQuart(e, t, n, r) { return -n * ((e = e / r - 1) * e * e * e - 1) + t }
                    static easeInOutQuart(e, t, n, r) { return (e /= r / 2) < 1 ? n / 2 * e * e * e * e + t : -n / 2 * ((e -= 2) * e * e * e - 2) + t }
                    static easeInQuint(e, t, n, r) { return n * (e /= r) * e * e * e * e + t }
                    static easeOutQuint(e, t, n, r) { return n * ((e = e / r - 1) * e * e * e * e + 1) + t }
                    static easeInOutQuint(e, t, n, r) { return (e /= r / 2) < 1 ? n / 2 * e * e * e * e * e + t : n / 2 * ((e -= 2) * e * e * e * e + 2) + t }
                    static easeInSine(e, t, n, r) { return -n * Math.cos(e / r * (Math.PI / 2)) + n + t }
                    static easeOutSine(e, t, n, r) { return n * Math.sin(e / r * (Math.PI / 2)) + t }
                    static easeInOutSine(e, t, n, r) { return -n / 2 * (Math.cos(Math.PI * e / r) - 1) + t }
                    static easeInExpo(e, t, n, r) { return 0 === e ? t : n * Math.pow(2, 10 * (e / r - 1)) + t }
                    static easeOutExpo(e, t, n, r) { return e === r ? t + n : n * (1 - Math.pow(2, -10 * e / r)) + t }
                    static easeInOutExpo(e, t, n, r) { return 0 === e ? t : e === r ? t + n : (e /= r / 2) < 1 ? n / 2 * Math.pow(2, 10 * (e - 1)) + t : n / 2 * (2 - Math.pow(2, -10 * --e)) + t }
                    static easeInCirc(e, t, n, r) { return -n * (Math.sqrt(1 - (e /= r) * e) - 1) + t }
                    static easeOutCirc(e, t, n, r) { return n * Math.sqrt(1 - (e = e / r - 1) * e) + t }
                    static easeInOutCirc(e, t, n, r) { return (e /= r / 2) < 1 ? -n / 2 * (Math.sqrt(1 - e * e) - 1) + t : n / 2 * (Math.sqrt(1 - (e -= 2) * e) + 1) + t }
                    static easeInElastic(e, t, n, r) {
                        let o = 1.70158,
                            i = 0,
                            s = n;
                        return 0 === e ? t : 1 == (e /= r) ? t + n : (i || (i = .3 * r), s < Math.abs(n) ? (s = n, o = i / 4) : o = i / (2 * Math.PI) * Math.asin(n / s), -s * Math.pow(2, 10 * (e -= 1)) * Math.sin((e * r - o) * (2 * Math.PI) / i) + t)
                    }
                    static easeOutElastic(e, t, n, r) {
                        let o = 1.70158,
                            i = 0,
                            s = n;
                        return 0 === e ? t : 1 == (e /= r) ? t + n : (i || (i = .3 * r), s < Math.abs(n) ? (s = n, o = i / 4) : o = i / (2 * Math.PI) * Math.asin(n / s), s * Math.pow(2, -10 * e) * Math.sin((e * r - o) * (2 * Math.PI) / i) + n + t)
                    }
                    static easeInOutElastic(e, t, n, r) {
                        let o = 1.70158,
                            i = 0,
                            s = n;
                        return 0 === e ? t : 2 == (e /= r / 2) ? t + n : (i || (i = r * (.3 * 1.5)), s < Math.abs(n) ? (s = n, o = i / 4) : o = i / (2 * Math.PI) * Math.asin(n / s), e < 1 ? s * Math.pow(2, 10 * (e -= 1)) * Math.sin((e * r - o) * (2 * Math.PI) / i) * -.5 + t : s * Math.pow(2, -10 * (e -= 1)) * Math.sin((e * r - o) * (2 * Math.PI) / i) * .5 + n + t)
                    }
                    static easeInBack(e, t, n, r, o) { return void 0 === o && (o = 1.70158), n * (e /= r) * e * ((o + 1) * e - o) + t }
                    static easeOutBack(e, t, n, r, o) { return void 0 === o && (o = 1.70158), n * ((e = e / r - 1) * e * ((o + 1) * e + o) + 1) + t }
                    static easeInOutBack(e, t, n, r, o) { return void 0 === o && (o = 1.70158), (e /= r / 2) < 1 ? n / 2 * (e * e * ((1 + (o *= 1.525)) * e - o)) + t : n / 2 * ((e -= 2) * e * ((1 + (o *= 1.525)) * e + o) + 2) + t }
                    static easeInBounce(e, t, n, r) { return n - this.easeOutBounce(r - e, 0, n, r) + t }
                    static easeOutBounce(e, t, n, r) { return (e /= r) < 1 / 2.75 ? n * (7.5625 * e * e) + t : e < 2 / 2.75 ? n * (7.5625 * (e -= 1.5 / 2.75) * e + .75) + t : e < 2.5 / 2.75 ? n * (7.5625 * (e -= 2.25 / 2.75) * e + .9375) + t : n * (7.5625 * (e -= 2.625 / 2.75) * e + .984375) + t }
                    static easeInOutBounce(e, t, n, r) { return e < r / 2 ? .5 * this.easeInBounce(2 * e, 0, n, r) + t : .5 * this.easeOutBounce(2 * e - r, 0, n, r) + .5 * n + t }
                }
                class a {
                    static get isMobile() { const e = /(iphone|ipod|ipad|android|iemobile|blackberry|bada)/.test(window.navigator.userAgent.toLowerCase()); return e || ["iPad Simulator", "iPhone Simulator", "iPod Simulator", "iPad", "iPhone", "iPod"].includes(navigator.platform) || navigator.userAgent.includes("Mac") && "ontouchend" in document }
                    static get Browser() { let e; const t = function(t) { let n = t.indexOf(e); if (-1 === n) return; const r = t.indexOf("rv:"); return "Trident" === e && -1 !== r ? parseFloat(t.substring(r + 3)) : parseFloat(t.substring(n + e.length + 1)) }; let n = {}; return n[function() { const t = [{ string: navigator.userAgent, subString: "Edge", identity: "Edge" }, { string: navigator.userAgent, subString: "MSIE", identity: "IE" }, { string: navigator.userAgent, subString: "Trident", identity: "IE" }, { string: navigator.userAgent, subString: "Firefox", identity: "Firefox" }, { string: navigator.userAgent, subString: "Opera", identity: "Opera" }, { string: navigator.userAgent, subString: "OPR", identity: "Opera" }, { string: navigator.userAgent, subString: "Chrome", identity: "Chrome" }, { string: navigator.userAgent, subString: "Safari", identity: "Safari" }]; for (let n = 0; n < t.length; n++) { let r = t[n].string; if (e = t[n].subString, -1 !== r.indexOf(t[n].subString)) return t[n].identity } return "Other" }()] = !0, n.version = t(navigator.userAgent) || t(navigator.appVersion) || "Unknown", n }
                    static toCamelCase(e) { return e.replace(/-([a-z])/g, (function(e) { return e[1].toUpperCase() })) }
                    static toDash(e) { return e.split(/(?=[A-Z])/).join("-").toLowerCase() }
                    static unescapeHTML(e) { return (new DOMParser).parseFromString(e, "text/html").documentElement.textContent }
                    static escapeHTML(e) { const t = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "/": "&#x2F;", "`": "&#x60;", "=": "&#x3D;" }; return String(e).replace(/[&<>"'`=\/]/g, (e => t[e])) }
                    static sanitizeHTML(e) { if (e && (e.indexOf("onclick") >= 0 || e.indexOf("onload") >= 0 || e.indexOf("onerror") >= 0)) return this.escapeHTML(e); const t = new RegExp("<s*(applet|audio|base|bgsound|embed|form|iframe|isindex|keygen|layout|link|meta|object|script|svg|style|template|video)[^>]*>(.*?)<s*/s*(applet|audio|base|bgsound|embed|form|iframe|isindex|keygen|layout|link|meta|object|script|svg|style|template|video)>", "ig"); return String(e).replace(t, (e => this.escapeHTML(e))) }
                    static createGUID() {
                        function e() { return Math.floor(65536 * (1 + Math.random())).toString(16).substring(1) }
                        return e() + e() + "-" + e() + "-" + e() + "-" + e() + "-" + e() + e() + e()
                    }
                    static getScriptLocation() {
                        return "./" !== window[n].BaseUrl ? window[n].BaseUrl : function() {
                            if (document.currentScript) {
                                let e = document.currentScript.src,
                                    t = e.lastIndexOf("/");
                                return e = e.substring(0, t), e
                            }
                            const e = new Error;
                            let t = "(",
                                n = ")";
                            if (Smart.Utilities.Core.Browser.Safari && (t = "@", n = "\n"), e.fileName) return e.fileName.replace("/smart.element.js", "");
                            let r = e.stack.split(t);
                            return r = r[1], r = r.split(n)[0], r = r.split(":"), r.splice(-2, 2), r = r.join(":"), r.replace("/smart.element.js", "")
                        }()
                    }
                    static CSSVariablesSupport() { return window.CSS && window.CSS.supports && window.CSS.supports("(--fake-var: 0)") }
                    static assign(e, t) {
                        const n = e => e && "object" == typeof e && !Array.isArray(e) && null !== e;
                        let r = Object.assign({}, e);
                        return n(e) && n(t) && Object.keys(t).forEach((o => {
                            n(t[o]) ? o in e ? r[o] = this.assign(e[o], t[o]) : Object.assign(r, {
                                [o]: t[o]
                            }) : Object.assign(r, {
                                [o]: t[o]
                            })
                        })), r
                    }
                    static html(e, t) {
                        const n = this;
                        let r = "",
                            o = e.childNodes;
                        if (!t) {
                            for (let e, t = 0, i = o.length; t < i && (e = o[t]); t++) {
                                const t = ["strong"];
                                if (e instanceof HTMLElement || e.tagName && t.indexOf(e.tagName.toLowerCase()) >= 0) {
                                    const t = e.tagName.toLowerCase(),
                                        o = e.attributes;
                                    let i = "<" + t;
                                    for (let e, t = 0; e = o[t]; t++) i += " " + e.name + '="' + e.value.replace(/[&\u00A0"]/g, y.Core.escapeHTML) + '"';
                                    i += ">", ["area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"][t] && (r += i), r = r + i + n.html(e) + "</" + t + ">"
                                } else {
                                    if (8 === e.nodeType) continue;
                                    r += e.textContent.replace(/[&\u00A0<>]/g, y.Core.escapeHTML)
                                }
                            }
                            return r
                        } {
                            const n = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi;
                            e.innerHTML = t.replace(n, "<$1></$2>")
                        }
                    }
                }
                let l = [];
                class d {
                    static watch(e) {
                        switch (e.nodeName.toLowerCase()) {
                            case "smart-grid":
                            case "smart-kanban":
                            case "smart-table":
                            case "smart-pivot-table":
                            case "smart-scheduler":
                            case "smart-tabs":
                            case "smart-card-view":
                            case "smart-list-box":
                            case "smart-combo-box":
                            case "smart-drop-down-list":
                            case "smart-calendar":
                            case "smart-gauge":
                            case "smart-numeric-text-box":
                            case "smart-menu":
                            case "smart-tree":
                                l.push(e);
                                break;
                            default:
                                return
                        }
                        d.start()
                    }
                    static start() { d.isStarted || (d.isStarted = !0, d.interval && clearInterval(d.interval), 0 === l.length || document.hidden ? d.isStarted = !1 : d.interval = setInterval((function() { d.observe() }), 100)) }
                    static stop() { d.isStarted = !1, d.interval && clearInterval(d.interval) }
                    static observeElement(e) {
                        const t = e;
                        if ("test" === window.Smart.Mode || document.hidden) return void(d.interval && clearInterval(d.interval));
                        let n = e._computedStyle || "resize" !== t.hasStyleObserver ? document.defaultView.getComputedStyle(t, null) : {},
                            r = !0,
                            o = "resize" !== t.hasStyleObserver ? ["paddingLeft", "paddingRight", "paddingTop", "paddingBottom", "borderLeftWidth", "borderRightWidth", "borderTopWidth", "borderBottomWidth", "display", "visibility", "font-size", "font-family", "font-style", "font-weight", "max-height", "min-height", "max-width", "min-width", "overflow", "overflow-x", "overflow-y"] : [];
                        if (e.styleProperties && (o = o.concat(e.styleProperties)), e.observableStyleProperties && (o = e.observableStyleProperties), !t._styleInfo) {
                            t._styleInfo = [];
                            for (let e = 0; e < o.length; e++) {
                                const r = o[e],
                                    i = r.startsWith("--") ? n.getPropertyValue(r) : n[r];
                                t._styleInfo[r] = i
                            }
                            return
                        }
                        if (e.isHidden || "none" !== n.display && (0 !== e.offsetWidth && 0 !== e.offsetHeight || (e.isHidden = !0)), e.isHidden) {
                            if (e.visibilityChangedHandler(), e.isHidden) return;
                            r = !1
                        }
                        let i = [];
                        for (let e = 0; e < o.length; e++) {
                            const r = o[e],
                                s = r.startsWith("--") ? n.getPropertyValue(r) : n[r];
                            t._styleInfo[r] !== s && (i[r] = { oldValue: t._styleInfo[r], value: s }, i.length++), t._styleInfo[r] = s
                        }
                        i.length > 0 && (t.$.fireEvent("styleChanged", { styleProperties: i }, { bubbles: !1, cancelable: !0 }), i.display && r && t.$.fireEvent("resize", t, { bubbles: !1, cancelable: !0 }))
                    }
                    static observe() {
                        for (let e = 0; e < l.length; e++) {
                            const t = l[e];
                            this.observeElement(t)
                        }
                    }
                    static unwatch(e) { d.stop(); const t = l.indexOf(e); - 1 !== t && l.splice(t, 1), d.start() }
                }
                let c = [];
                const u = [],
                    p = ["resize", "down", "up", "move", "tap", "taphold", "swipeleft", "swiperight", "swipetop", "swipebottom"];
                class h {
                    constructor(e) {
                        const t = this;
                        t.target = e, t.$target = new f(e), t.$document = e.$document ? e.$document : new f(document), t.id = (Date.now().toString(36) + Math.random().toString(36).substr(2, 5)).toUpperCase();
                        let n = { handlers: {}, boundEventTypes: [], listen: t.listen.bind(t), unlisten: t.unlisten.bind(t) };
                        return t.tapHoldDelay = 750, t.swipeMin = 10, t.swipeMax = 5e3, t.swipeDelay = 1e3, t.tapHoldDelay = 750, t.inputEventProperties = ["clientX", "clientY", "pageX", "pageY", "screenX", "screenY"], p.forEach((e => {
                            n[e] = t => { n.handlers[e] = t }, t[e] = e => {
                                if (!n.handlers[e.type]) {
                                    if (("mousemove" === e.type || "pointermove" === e.type || "touchmove" === e.type) && n.handlers.move) {
                                        const r = t.createEvent(e, "move");
                                        n.handlers.move(r)
                                    }
                                    return !0
                                }
                                return n.handlers[e.type](e)
                            }
                        })), t.listen(), t.handlers = n.handlers, n
                    }
                    listen(e) {
                        const t = this;
                        if ("resize" === e && t.target !== document && t.target !== window && !1 !== t.target.hasResizeObserver)
                            if (Smart.Utilities.Core.Browser.Firefox) {
                                if (!t.target.resizeObserver) {
                                    let e, n, r, o = !1,
                                        i = t.target.offsetWidth,
                                        s = t.target.offsetHeight;
                                    const a = new ResizeObserver((() => {
                                        if (!o) return void(o = !0);
                                        const a = new CustomEvent("resize", { bubbles: !1, cancelable: !0 });
                                        n = t.target.offsetWidth, r = t.target.offsetHeight, e = n !== i || r !== s, t.target.requiresLayout && (e = !0), e && (t.resize(a), t.target.requiresLayout = !1)
                                    }));
                                    a.observe(t.target), t.target.resizeObserver = a
                                }
                            } else if (!t.target.resizeTrigger) {
                            const e = document.createElement("div");
                            e.className = "smart-resize-trigger-container", e.innerHTML = '<div class="smart-resize-trigger-container"><div class="smart-resize-trigger"></div></div><div class="smart-resize-trigger-container"><div class="smart-resize-trigger-shrink"></div></div>', e.setAttribute("aria-hidden", !0), window[n].EnableShadowDOM && t.target.shadowRoot ? t.target.shadowRoot.appendChild(e) : t.target.appendChild(e), t.target.resizeTrigger = e;
                            const r = e.childNodes[0],
                                o = r.childNodes[0],
                                i = e.childNodes[1],
                                s = function() { o.style.width = "100000px", o.style.height = "100000px", r.scrollLeft = 1e5, r.scrollTop = 1e5, i.scrollLeft = 1e5, i.scrollTop = 1e5 };
                            let a, l, d, c, u = t.target.offsetWidth,
                                p = t.target.offsetHeight;
                            if (0 === u || 0 === p) {
                                const e = function() { s(), t.target.removeEventListener("resize", e) };
                                t.target.addEventListener("resize", e), s()
                            } else s();
                            t.target.resizeHandler = function() {
                                l || (l = requestAnimationFrame((function() {
                                    if (l = 0, d = t.target.offsetWidth, c = t.target.offsetHeight, a = d !== u || c !== p, t.target.requiresLayout && (a = !0), !a) return;
                                    u = d, p = c;
                                    const e = new CustomEvent("resize", { bubbles: !1, cancelable: !0 });
                                    t.resize(e), t.target.requiresLayout = !1
                                }))), s()
                            }, r.addEventListener("scroll", t.target.resizeHandler), i.addEventListener("scroll", t.target.resizeHandler)
                        }
                        t.isListening || (t.isListening = !0, t.isPressed = !1, t.isReleased = !1, t.isInBounds = !1, window.PointerEvent ? (t.$target.listen("pointerdown.inputEvents" + t.id, t.pointerDown.bind(t)), t.$target.listen("pointerup.inputEvents" + t.id, t.pointerUp.bind(t)), t.$target.listen("pointermove.inputEvents" + t.id, t.pointerMove.bind(t)), t.$target.listen("pointercancel.inputEvents" + t.id, t.pointerCancel.bind(t))) : ("ontouchstart" in window && (t.$target.listen("touchmove.inputEvents" + t.id, t.touchMove.bind(t)), t.$target.listen("touchstart.inputEvents" + t.id, t.touchStart.bind(t)), t.$target.listen("touchend.inputEvents" + t.id, t.touchEnd.bind(t)), t.$target.listen("touchcancel.inputEvents" + t.id, t.touchCancel.bind(t))), t.$target.listen("mousedown.inputEvents" + t.id, t.mouseDown.bind(t)), t.$target.listen("mouseup.inputEvents" + t.id, t.mouseUp.bind(t)), t.$target.listen("mousemove.inputEvents" + t.id, t.mouseMove.bind(t)), t.$target.listen("mouseleave.inputEvents" + t.id, t.mouseLeave.bind(t))), t.target._handleDocumentUp || (t.target._handleDocumentUp = t.handleDocumentUp.bind(t), t.target._handleDocumentUpId = t.id, t.$document.listen("mouseup.inputEvents" + t.target._handleDocumentUpId, t.target._handleDocumentUp)))
                    }
                    unlisten(e) {
                        const t = this;
                        if (t.isListening = !1, window.PointerEvent ? (t.$target.unlisten("pointerdown.inputEvents" + t.id), t.$target.unlisten("pointerup.inputEvents" + t.id), t.$target.unlisten("pointermove.inputEvents" + t.id), t.$target.unlisten("pointercancel.inputEvents" + t.id)) : ("ontouchstart" in window && (t.$target.unlisten("touchstart.inputEvents" + t.id), t.$target.unlisten("touchmove.inputEvents" + t.id), t.$target.unlisten("touchend.inputEvents" + t.id), t.$target.unlisten("touchcancel.inputEvents" + t.id)), t.$target.unlisten("mousedown.inputEvents" + t.id), t.$target.unlisten("mouseup.inputEvents" + t.id), t.$target.unlisten("mousemove.inputEvents" + t.id), t.$target.unlisten("mouseleave.inputEvents" + t.id)), t.target._handleDocumentUp && (t.$document.unlisten("mouseup.inputEvents" + t.target._handleDocumentUpId, t.target._handleDocumentUp), delete t.target._handleDocumentUp, delete t.target._handleDocumentUpId), "resize" === e)
                            if (Smart.Utilities.Core.Browser.Firefox) t.target.resizeObserver && (t.target.resizeObserver.unobserve(t.target), delete t.target.resizeObserver);
                            else if (t.target.resizeTrigger) {
                            const e = t.target.resizeTrigger,
                                n = e.childNodes[0],
                                r = e.childNodes[1];
                            n.removeEventListener("scroll", t.target.resizeHandler), r.removeEventListener("scroll", t.target.resizeHandler), t.target.resizeHandler = null, e.parentNode.removeChild(e), delete t.target.resizeTrigger
                        }
                    }
                    handleDocumentUp(e) {
                        const t = this;
                        t.isPressed = !1, t.isReleased = !1, t.resetSwipe(e)
                    }
                    createEvent(e, t) {
                        const n = this,
                            r = e.touches,
                            o = e.changedTouches,
                            i = r && r.length ? r[0] : o && o.length ? o[0] : void 0,
                            s = new CustomEvent(t, { bubbles: !0, cancelable: !0, composed: void 0 !== n.$target.element.getRootNode().host });
                        if (s.originalEvent = e, i) {
                            for (let e = 0; e < n.inputEventProperties.length; e++) {
                                const t = n.inputEventProperties[e];
                                s[t] = i[t]
                            }
                            return s
                        }
                        for (let t in e) t in s || (s[t] = e[t]);
                        return s
                    }
                    fireTap(e) {
                        const t = this;
                        if (clearTimeout(this.tapHoldTimeout), !this.tapHoldFired && this.isInBounds) {
                            const n = t.createEvent(e, "tap");
                            t.tap(n)
                        }
                    }
                    initTap(e) {
                        const t = this;
                        t.isInBounds = !0, t.tapHoldFired = !1, t.tapHoldTimeout = setTimeout((function() {
                            if (t.isInBounds) {
                                t.tapHoldFired = !0;
                                const n = t.createEvent(e, "taphold");
                                t.taphold(n)
                            }
                        }), t.tapHoldDelay)
                    }
                    pointerDown(e) { return this.handleDown(e) }
                    mouseDown(e) { const t = this; if (!(t.isPressed || t.touchStartTime && new Date - t.touchStartTime < 500)) return t.handleDown(e) }
                    touchStart(e) { const t = this; return t.touchStartTime = new Date, t.isTouchMoved = !0, t.handleDown(e) }
                    mouseUp(e) { const t = this; if (!(t.isReleased || t.touchEndTime && new Date - t.touchEndTime < 500)) return t.handleUp(e) }
                    handleDown(e) {
                        const t = this;
                        t.isReleased = !1, t.isPressed = !0;
                        const n = t.createEvent(e, "down");
                        return (t.handlers.tap || t.handlers.taphold) && t.initTap(n), (t.handlers.swipeleft || t.handlers.swiperight || t.handlers.swipetop || t.handlers.swipebottom) && t.initSwipe(n), t.down(n)
                    }
                    handleUp(e) {
                        const t = this;
                        t.isReleased = !0, t.isPressed = !1;
                        const n = t.createEvent(e, "up"),
                            r = t.up(n);
                        return (t.handlers.tap || t.handlers.taphold) && t.fireTap(n), t.resetSwipe(n), r
                    }
                    handleMove(e) { const t = this; let n = t.move(e); return t.isPressed && (t._maxSwipeVerticalDistance = Math.max(t._maxSwipeVerticalDistance, Math.abs(t._startY - e.pageY)), t._maxSwipeHorizontalDistance = Math.max(t._maxSwipeHorizontalDistance, Math.abs(t._startX - e.pageX)), n = t.handleSwipeEvents(e)), n }
                    touchEnd(e) { return this.touchEndTime = new Date, this.handleUp(e) }
                    pointerUp(e) { return this.handleUp(e) }
                    pointerCancel(e) { this.pointerUp(e) }
                    touchCancel(e) { this.touchEnd(e) }
                    mouseLeave() { this.isInBounds = !1 }
                    mouseMove(e) { if (!this.isTouchMoved) return this.handleMove(e) }
                    pointerMove(e) { return this.handleMove(e) }
                    touchMove(e) {
                        const t = this,
                            n = e.touches,
                            r = e.changedTouches,
                            o = n && n.length ? n[0] : r && r.length ? r[0] : void 0;
                        for (let n = 0; n < t.inputEventProperties.length; n++) {
                            const r = t.inputEventProperties[n];
                            void 0 === e[r] && (e[r] = o[r])
                        }
                        return t.isTouchMoved = !0, t.handleMove(e)
                    }
                    handleSwipeEvents(e) { const t = this; let n = !0; return (t.handlers.swipetop || t.handlers.swipebottom) && (n = this.handleVerticalSwipeEvents(e)), !1 === n || (t.handlers.swipeleft || t.handlers.swiperight) && (n = this.handleHorizontalSwipeEvents(e)), n }
                    handleVerticalSwipeEvents(e) { let t, n; return t = e.pageY, n = t - this._startY, this.swiped(e, n, "vertical") }
                    handleHorizontalSwipeEvents(e) { let t, n; return t = e.pageX, n = t - this._startX, this.swiped(e, n, "horizontal") }
                    swiped(e, t, n) { const r = this; if (n = n || 0, Math.abs(t) >= r.swipeMin && !r._swipeEvent && !r._swipeLocked) { let o = t < 0 ? "swipeleft" : "swiperight"; if ("horizontal" === n ? r._swipeEvent = r.createEvent(e, o) : (o = t < 0 ? "swipetop" : "swipebottom", r._swipeEvent = r.createEvent(e, t < 0 ? "swipetop" : "swipebottom")), r[o] && (r[o](this._swipeEvent), Math.abs(t) <= this.swipeMax)) return e.stopImmediatePropagation(), !1 } return !0 }
                    resetSwipe() { this._swipeEvent = null, clearTimeout(this._swipeTimeout) }
                    initSwipe(e) {
                        const t = this;
                        t._maxSwipeVerticalDistance = 0, t._maxSwipeHorizontalDistance = 0, t._startX = e.pageX, t._startY = e.pageY, t._swipeLocked = !1, t._swipeEvent = null, t._swipeTimeout = setTimeout((function() { t._swipeLocked = !0 }), t.swipeDelay)
                    }
                }
                class m {
                    get scrollWidth() { const e = this; return e.horizontalScrollBar ? e.horizontalScrollBar.max : -1 }
                    set scrollWidth(e) {
                        const t = this;
                        e < 0 && (e = 0), t.horizontalScrollBar && (t.horizontalScrollBar.max = e)
                    }
                    get scrollHeight() { const e = this; return e.verticalScrollBar ? e.verticalScrollBar.max : -1 }
                    set scrollHeight(e) {
                        const t = this;
                        e < 0 && (e = 0), t.verticalScrollBar && (t.verticalScrollBar.max = e)
                    }
                    get scrollLeft() { const e = this; return e.horizontalScrollBar ? e.horizontalScrollBar.value : -1 }
                    set scrollLeft(e) {
                        const t = this;
                        e < 0 && (e = 0), t.horizontalScrollBar && (t.horizontalScrollBar.value = e)
                    }
                    get scrollTop() { const e = this; return e.verticalScrollBar ? e.verticalScrollBar.value : -1 }
                    set scrollTop(e) {
                        const t = this;
                        e < 0 && (e = 0), t.verticalScrollBar && (t.verticalScrollBar.value = e)
                    }
                    get vScrollBar() { return this.verticalScrollBar }
                    get hScrollBar() { return this.horizontalScrollBar }
                    constructor(e, t, n) {
                        const r = this;
                        r.container = e, r.horizontalScrollBar = t, r.verticalScrollBar = n, r.disableSwipeScroll = !1, r.listen()
                    }
                    listen() {
                        const e = this,
                            t = a.isMobile,
                            n = e.horizontalScrollBar,
                            r = e.verticalScrollBar;
                        let o, i, s, l, d, c, u, p;
                        e.inputEvents = new h(e.container);
                        const m = function(e) { return { amplitude: 0, delta: 0, initialValue: 0, min: 0, max: e.max, previousValue: 0, pointerPosition: 0, targetValue: 0, scrollBar: e, value: 0, velocity: 0 } },
                            f = m(n),
                            g = m(r),
                            w = function() {
                                const t = e.container.touchVelocityCoefficient || 50;
                                c = Date.now(), u = c - l, l = c;
                                const n = function(e) {
                                    e.delta = e.value - e.previousValue, e.previousValue = e.value;
                                    let n = t * e.delta / (1 + u);
                                    e.velocity = .8 * n + .2 * e.velocity
                                };
                                n(g), n(f)
                            },
                            b = function(e) { return p.value = e > p.max ? p.max : e < p.min ? p.min : e, p.scrollBar.value = p.value, e > p.max ? "max" : e < p.min ? "min" : "value" };

                        function v() {
                            let t, n;
                            p.amplitude && (e.container.$.fireEvent("kineticScroll"), t = Date.now() - l, n = -p.amplitude * Math.exp(-t / 500), n > 5 || n < -5 ? (b(p.targetValue + n), cancelAnimationFrame(i), i = 0, i = requestAnimationFrame(v)) : b(p.targetValue))
                        }
                        let _;
                        e.inputEvents.down((function(n) {
                            if (!t) return;
                            const r = n.originalEvent.target,
                                i = r && r.closest ? r.closest("smart-scroll-bar") : void 0;
                            if (i === e.horizontalScrollBar || i === e.verticalScrollBar) return;
                            s = !0, o = !1;
                            const a = function(e, t) { e.amplitude = 0, e.pointerPosition = t, e.previousValue = e.value, e.value = e.scrollBar.value, e.initialValue = e.value, e.max = e.scrollBar.max };
                            a(g, n.clientY), a(f, n.clientX), l = Date.now(), clearInterval(d), d = setInterval(w, 500)
                        })), e.inputEvents.up((function() {
                            if (!s) return !0;
                            if (clearInterval(d), e.disableSwipeScroll) return void(s = !1);
                            const t = function(e) { p = e, e.amplitude = .8 * e.velocity, e.targetValue = Math.round(e.value + e.amplitude), l = Date.now(), cancelAnimationFrame(i), i = requestAnimationFrame(v), e.velocity = 0 };
                            g.velocity > 10 || g.velocity < -10 ? t(g) : (f.velocity > 10 || f.velocity < -10) && t(f), s = !1
                        })), e.inputEvents.move((function(t) {
                            if (!s) return !0;
                            if (e.disableSwipeScroll) return;
                            if (o && (t.originalEvent.preventDefault(), t.originalEvent.stopPropagation()), f.visible = e.scrollWidth > 0, g.visible = e.scrollHeight > 0, !s || !f.visible && !g.visible) return;
                            const n = e.container.touchScrollRatio,
                                r = e.container;
                            let i, a;
                            n && ("number" == typeof n ? (i = -n, a = -n) : "function" == typeof n && (i = n(g.max, r.offsetHeight), a = n(f.max, r.offsetWidth))), g.ratio = i || -g.max / r.offsetHeight, g.delta = (t.clientY - g.pointerPosition) * g.ratio, f.ratio = a || -f.max / r.offsetWidth, f.delta = (t.clientX - f.pointerPosition) * f.ratio;
                            let l = "value";
                            const d = function(t, n, r) { return t.delta > 5 || t.delta < -5 ? (p = t, l = t.initialValue + t.delta > p.max ? "max" : t.initialValue + t.delta < p.min ? "min" : "value", "min" === l && 0 === t.initialValue || "max" === l && t.initialValue === t.max || !t.visible || (e.container.$.fireEvent("kineticScroll"), b(t.initialValue + t.delta), w(), r.originalEvent.preventDefault(), r.originalEvent.stopPropagation(), o = !0, !1)) : null };
                            let c = d(g, t.clientY, t);
                            if (null !== c) return c; { let e = d(f, t.clientX, t); if (null !== e) return e }
                        })), e.scrollTo = function(t, n) {
                            const r = !1 === n ? f : g;
                            let o = !1;
                            l || (l = Date.now()), _ || (_ = Date.now()), Math.abs(Date.now() - _) > 375 ? l = Date.now() : o = !0, _ = Date.now(), r.value = r.scrollBar.value, r.delta = t - r.value, r.max = r.scrollBar.max, t <= r.min && (t = r.min), t >= r.max && (t = r.max), r.targetValue = t;
                            const s = t;
                            let a = r.value;
                            r.velocity = 100 * r.delta / (1 + r.max), r.from = a;
                            const d = function(e) { return r.value = e > r.max ? r.max : e < r.min ? r.min : e, r.scrollBar.value = r.value, e > r.max ? "max" : e < r.min ? "min" : "value" },
                                c = function() {
                                    let n, u = Date.now() - _,
                                        p = Math.min(1e3, Date.now() - l),
                                        h = r.velocity * Math.exp(p / 175);
                                    if (o)(h < 0 && r.value <= t || h > 0 && r.value >= t) && (h = 0), (r.value + h <= r.min || r.value + h >= r.max) && (h = 0), h > .5 || h < -.5 ? (d(r.value + h), cancelAnimationFrame(i), i = 0, i = requestAnimationFrame(c)) : d(r.targetValue);
                                    else {
                                        if (u >= 175) return cancelAnimationFrame(i), e.container.$.fireEvent("kineticScroll"), void(i = 0);
                                        n = y.Animation.Easings.easeInSine(u, a, s - a, 175), d(n), cancelAnimationFrame(i), i = 0, i = requestAnimationFrame(c)
                                    }
                                };
                            cancelAnimationFrame(i), i = requestAnimationFrame(c)
                        }, e.inputEvents.listen()
                    }
                    unlisten() {
                        const e = this;
                        e.inputEvents && e.inputEvents.unlisten(), delete e.inputEvents
                    }
                }
                class f {
                    constructor(e) { this.events = {}, this.handlers = {}, this.element = e }
                    hasClass(e) {
                        const t = this,
                            n = e.split(" ");
                        for (let e = 0; e < n.length; e++)
                            if (!t.element.classList.contains(n[e])) return !1;
                        return !0
                    }
                    addClass(e) {
                        const t = this;
                        if (t.hasClass(e)) return;
                        const n = e.split(" ");
                        for (let e = 0; e < n.length; e++) t.element.classList.add(n[e]);
                        t.isNativeElement || d.observeElement(t.element)
                    }
                    removeClass(e) { const t = this; if (0 === arguments.length) return void t.element.removeAttribute("class"); const n = e.split(" "); for (let e = 0; e < n.length; e++) t.element.classList.remove(n[e]); "" === t.element.className && t.element.removeAttribute("class"), t.isNativeElement || d.observeElement(t.element) }
                    get isCustomElement() { const e = this; return !!e.element.tagName.startsWith(n) || e.element instanceof window[n].BaseElement == 1 || "DIV" !== e.element.tagName && "SPAN" !== e.element.tagName && "BUTTON" !== e.element.tagName && "INPUT" !== e.element.tagName && "UL" !== e.element.tagName && "LI" !== e.element.tagName && document.createElement(e.element.nodeName) instanceof window[n].BaseElement == 1 }
                    get isNativeElement() { return !this.isCustomElement }
                    dispatch(e) {
                        const t = this,
                            n = t.events[e.type];
                        let r = !1;
                        if (n.length > 1)
                            for (let e = 0; e < n.length; e++) { const t = n[e]; if (t.namespace && t.namespace.indexOf("_") >= 0) { r = !0; break } }
                        r && n.sort((function(e, t) {
                            let n = e.namespace,
                                r = t.namespace;
                            return n = -1 === n.indexOf("_") ? 0 : parseInt(n.substring(n.indexOf("_") + 1)), r = -1 === r.indexOf("_") ? 0 : parseInt(r.substring(r.indexOf("_") + 1)), n < r ? -1 : n > r ? 1 : 0
                        }));
                        for (let r = 0; r < n.length; r++) { const o = n[r]; if (e.namespace = o.namespace, e.context = o.context, e.defaultPrevented) break; const i = o.handler.apply(t.element, [e]); if (void 0 !== i && (e.result = i, !1 === i)) { e.preventDefault(), e.stopPropagation(); break } }
                        return e.result
                    }
                    fireEvent(e, t, n) {
                        const r = this;
                        n || (n = { bubbles: !0, cancelable: !0, composed: null !== r.element.getRootNode().host }), n.detail = t || {};
                        const o = new CustomEvent(e, n);
                        return o.originalStopPropagation = o.stopPropagation, o.stopPropagation = function() { return o.isPropagationStopped = !0, o.originalStopPropagation() }, r.dispatchEvent(o), o
                    }
                    get isPassiveSupported() {
                        const e = this;
                        if (void 0 !== e.supportsPassive) return e.supportsPassive;
                        e.supportsPassive = !1;
                        try {
                            let t = Object.defineProperty({}, "passive", { get: function() { e.supportsPassive = !0 } });
                            window.addEventListener("testPassive", null, t), window.removeEventListener("testPassive", null, t)
                        } catch (e) {}
                        return e.supportsPassive
                    }
                    dispatchEvent(e) {
                        const t = this,
                            n = e.type,
                            r = t.element.context,
                            o = n.substring(0, 1).toUpperCase() + n.substring(1);
                        t.element.context = document, t.element["on" + o] ? t.element["on" + o](e) : t.element["on" + n.toLowerCase()] ? t.element["on" + n.toLowerCase()](e) : t.element.dispatchEvent(e), t.element.context = r
                    }
                    listen(e, t) {
                        const n = this,
                            r = e.split("."),
                            o = r.slice(1).join("."),
                            i = r[0];
                        n.events[i] || (n.events[i] = []);
                        const s = { type: i, handler: t, context: n.element, namespace: o };
                        p.indexOf(i) >= 0 && (n.inputEvents || (n.inputEvents = new h(n.element)), n.inputEvents[i]((function(e) { n.dispatchEvent(e) })), n.inputEvents.boundEventTypes.push(i), n.inputEvents.listen(i)), 0 === n.events[i].length && (n.handlers[i] = n.dispatch.bind(n), "wheel" === i ? n.element.addEventListener("wheel", n.handlers[i], !!n.isPassiveSupported && { passive: !1 }) : "touchmove" === i || "touchstart" === i || "touchend" === i ? n.element.addEventListener(i, n.handlers[i], !!n.isPassiveSupported && { passive: !1 }) : n.element.addEventListener(i, n.handlers[i], !1)), n.events[i].push(s)
                    }
                    unlisten(e) {
                        const t = this,
                            n = e.split("."),
                            r = n.slice(1).join("."),
                            o = n[0];
                        let i = t.events[o];
                        if (t.inputEvents && t.inputEvents.boundEventTypes.indexOf(o) >= 0 && (t.inputEvents.boundEventTypes.splice(t.inputEvents.boundEventTypes.indexOf(o), 1), 0 === t.inputEvents.boundEventTypes.length && t.inputEvents.unlisten(o)), i) {
                            for (let e = 0; e < i.length; e++) {
                                if ("" !== r) {
                                    let e = i.findIndex((e => e.namespace === r));
                                    i.splice(e, 1);
                                    break
                                }
                                i = []
                            }
                            0 === i.length && (t.element.removeEventListener(o, t.handlers[o]), t.events[o] = [], delete t.handlers[o])
                        }
                    }
                    getAttributeValue(e, t) {
                        const n = this,
                            r = n.element.getAttribute(e);
                        if (n.isNativeElement) return n.deserialize(r, t);
                        const o = n.element.propertyByAttributeName[e];
                        return void 0 === o.deserialize ? n.deserialize(r, t, o.nullable) : n.element[o.deserialize](r)
                    }
                    setAttributeValue(e, t, n) {
                        const r = this;
                        let o, i = !1;
                        if (r.isNativeElement) { if (o = r.serialize(t, n), "boolean" === n && ["checked", "selected", "async", "autofocus", "autoplay", "controls", "defer", "disabled", "hidden", "ismap", "loop", "multiple", "open", "readonly", "required", "scoped"].indexOf(e) >= 0) return void(t ? r.element.setAttribute(e, "") : r.element.removeAttribute(e)) } else {
                            const s = r.element.propertyByAttributeName[e];
                            i = !s || s.nullable, o = s && s.serialize ? r.element[s.serialize](t) : r.serialize(t, n, i)
                        }
                        "array" !== n && "object" !== n || "[]" !== o && "{}" !== o ? void 0 === o ? (r.element.removeAttribute(e), r.element.shadowRoot && r.element.$.root && r.element.$.root.removeAttribute(e)) : (r.element.setAttribute(e, o), r.element.shadowRoot && r.element.$.root && r.element.$.root.setAttribute(e, o)) : r.element.removeAttribute(e)
                    }
                    serialize(e, t, n) { if (void 0 === t && (t = y.Types.getType(e)), void 0 !== e && (n || null !== e)) { if (n && null === e) return "null"; if ("string" === t) return e; if ("boolean" === t || "bool" === t) { if (!0 === e || "true" === e || 1 === e || "1" === e) return ""; if (!1 === e || "false" === e || 0 === e || "0" === e) return } return "array" === t ? JSON.stringify(e) : ["string", "number", "int", "integer", "float", "date", "any", "function"].indexOf(t) >= 0 ? e.toString() : "object" === t ? JSON.stringify(e) : void 0 } }
                    deserialize(e, t, n) {
                        const r = "null" === e;
                        if (void 0 !== e && (!r || n)) {
                            if (r && n) return null;
                            if ("boolean" === t || "bool" === t) return null !== e;
                            if ("number" === t || "float" === t) return "NaN" === e ? NaN : "Infinity" === e ? 1 / 0 : "-Infinity" === e ? -1 / 0 : parseFloat(e);
                            if ("int" === t || "integer" === t) return "NaN" === e ? NaN : "Infinity" === e ? 1 / 0 : "-Infinity" === e ? -1 / 0 : parseInt(e);
                            if ("string" === t) return e;
                            if ("any" === t) return e;
                            if ("date" === t) return new Date(e);
                            if ("function" === t) { if ("function" == typeof window[e]) return window[e] } else if ("array" === t || "object" === t) try { const t = JSON.parse(e); if (t) return t } catch (n) {
                                if (window[e] && "object" == typeof window[e]) return window[e];
                                if ("array" === t && e.indexOf("[") >= 0) {
                                    if (e.indexOf("{") >= 0) {
                                        let t = e.replace(/{/gi, "").replace("[", "").replace("]", "").replace(/'/gi, "").replace(/"/gi, "").trim();
                                        t = t.split("},");
                                        for (let e = 0; e < t.length; e++) {
                                            let n = {},
                                                r = t[e].trim().split(",");
                                            for (let e = 0; e < r.length; e++) {
                                                const t = r[e].split(":")[0].trim(),
                                                    o = r[e].split(":")[1].trim();
                                                n[t] = o
                                            }
                                            t[e] = n
                                        }
                                        return t
                                    }
                                    return e.replace("[", "").replace("]", "").replace(/'/gi, "").replace(/"/gi, "").trim().split(",")
                                }
                            }
                        }
                    }
                }
                class g {
                    static get Ripple() { return i }
                    static get Easings() { return s }
                }
                class y {
                    static get Types() { return o }
                    static get Core() { return a }
                    static get Animation() { return g }
                    static get Scroll() { return m }
                    static get InputEvents() { return h }
                    static Extend(e) { return new f(e) }
                    static Assign(e, t) {
                        if (e.indexOf(".") >= 0) { const n = e.split("."); return y[n[0]] || (y[n[0]] = {}), void(y[n[0]][n[1]] = t) }
                        y[e] = t
                    }
                }
                const w = y.Extend(document);
                let b = null;
                document.addEventListener("click", (() => { d.start(), b && clearTimeout(b), b = setTimeout((() => { d.stop() }), 1e4) })), document.addEventListener("mouseenter", (() => { d.start() })), document.addEventListener("mouseleave", (() => { d.stop() }));
                class v {}
                v.cache = {};
                class _ extends HTMLElement {
                    static get properties() { return { animation: { value: "advanced", type: "string", allowedValues: ["none", "simple", "advanced"] }, unfocusable: { value: !1, type: "boolean" }, disabled: { value: !1, type: "boolean" }, dataContext: { value: null, reflectToAttribute: !1, type: "any" }, debugMode: { value: !0, type: "boolean", reflectToAttribute: !1 }, locale: { value: "en", type: "string", reflectToAttribute: !1 }, localizeFormatFunction: { value: void 0, type: "function", reflectToAttribute: !1 }, messages: { value: { en: { propertyUnknownName: "Invalid property name: '{{name}}'!", propertyUnknownType: "'{{name}}' property is with undefined 'type' member!", propertyInvalidValue: "Invalid '{{name}}' property value! Actual value: '{{actualValue}}', Expected value: '{{value}}'!", propertyInvalidValueType: "Invalid '{{name}}' property value type! Actual type: '{{actualType}}', Expected type: '{{type}}'!", methodInvalidValueType: "Invalid '{{name}}' method argument value type! Actual type: '{{actualType}}', Expected type: '{{type}}' for argument with index: '{{argumentIndex}}'!", methodInvalidArgumentsCount: "Invalid '{{name}}' method arguments count! Actual arguments count: '{{actualArgumentsCount}}', Expected at least: '{{argumentsCount}}' argument(s)!", methodInvalidReturnType: "Invalid '{{name}}' method return type! Actual type: '{{actualType}}', Expected type: '{{type}}'!", elementNotInDOM: "Element does not exist in DOM! Please, add the element to the DOM, before invoking a method.", moduleUndefined: "Module is undefined.", missingReference: "{{elementType}}: Missing reference to '{{files}}'.", htmlTemplateNotSuported: "{{elementType}}: Web Browser doesn't support HTMLTemplate elements.", invalidTemplate: "{{elementType}}: '{{property}}' property accepts a string that must match the id of an HTMLTemplate element from the DOM." } }, reflectToAttribute: !1, inherit: !0, type: "object" }, props: { value: null, reflectToAttribute: !1, isHierarchicalProperty: !0, type: "any" }, readonly: { value: !1, type: "boolean" }, renderMode: { value: "auto", type: "string", reflectToAttribute: !1, allowedValues: ["auto", "manual"] }, rightToLeft: { value: !1, type: "boolean" }, rethrowError: { value: !0, type: "boolean", reflectToAttribute: !1 }, theme: { value: window[n].Theme, type: "string" }, visibility: { value: "visible", allowedValues: ["visible", "collapsed", "hidden"], type: "string" }, wait: { value: !1, type: "boolean" } } }
                    getBindings(e, t) {
                        const n = this;
                        let r = 0,
                            o = {},
                            i = (e => { if (e instanceof HTMLElement) return n.parseAttributes(e); { let t = n.parseProperty(e.data ? e.data.trim() : null, "textContent", e); if (t) return n && e.parentNode === n.$.content && (t.value = "" !== n.$.html ? n.$.html : void 0, n.innerHTML = ""), { textContent: t } } })(e);
                        i && (o.data = i), t || (o.mapping = [], t = o), e.getAttribute && (o.nodeId = e.getAttribute("smart-id"), t && i && (t.mapping[o.nodeId] = i)), o.node = e, e.firstChild && (o.children = {});
                        for (let i = e.firstChild; i; i = i.nextSibling) o.children[r++] = n.getBindings(i, t);
                        return o
                    }
                    _addRemovePropertyBinding(e, t, n, r, o) {
                        if (!e || !t || !n) return;
                        const i = this,
                            s = i.bindings,
                            a = n.getAttribute("smart-id"),
                            l = e.indexOf("{{") >= 0;
                        let d = !1;
                        (e = e.replace("{{", "").replace("}}", "").replace("[[", "").replace("]]", "")).indexOf("!") >= 0 && (e = e.replace("!", ""), d = !0);
                        const c = i._properties[e],
                            u = { name: e, reflectToAttribute: c.reflectToAttribute, twoWay: l, type: c.type, not: d };
                        if (o && !r) {
                            const n = {},
                                r = { name: e, targetPropertyName: t, reflectToAttribute: c.reflectToAttribute, twoWay: l, type: c.type, not: d };
                            n[e] = r, s.mapping[a] = n
                        }
                        const p = function(e) {
                            for (let o in e) {
                                const s = e[o];
                                if (s.nodeId === a) { s.data || (s.data = {}), r ? (s.data[t] = null, delete s.data[t]) : s.data[t] = u; break }
                                if (s.children) p(s.children);
                                else if (s.node && s.node.children && s.node === n.parentElement) {
                                    const e = s.node;
                                    if (!e.firstChild) continue;
                                    s.children = {};
                                    let t = 0;
                                    for (let n = e.firstChild; n; n = n.nextSibling) s.children[t++] = i.getBindings(n);
                                    p(s.children)
                                }
                            }
                        };
                        p(s.children), r ? delete i.boundProperties[e] : i.boundProperties[e] = !0, i.updateBoundNodes(e)
                    }
                    addPropertyBinding(e, t, n, r) { this._addRemovePropertyBinding(e, t, n, !1, r) }
                    removePropertyBinding(e, t, n, r) { this._addRemovePropertyBinding(e, t, n, !0, r) }
                    parseAttributes(e) {
                        const t = this;
                        let n;
                        for (let r = 0; r < e.attributes.length; r++) {
                            const o = e.attributes[r],
                                i = o.name,
                                s = o.value;
                            v.cache["toCamelCase" + i] || (v.cache["toCamelCase" + i] = y.Core.toCamelCase(i));
                            const a = v.cache["toCamelCase" + i];
                            if (i.indexOf("(") >= 0) {
                                let r = i.substring(1, i.length - 1);
                                if (t && !t.dataContext) { t.templateListeners[e.getAttribute("smart-id") + "." + r] = s, e.removeAttribute(i); continue } {
                                    n || (n = {});
                                    const e = s.substring(0, s.indexOf("("));
                                    n[a] = { isEvent: !0, name: r, value: e };
                                    continue
                                }
                            }
                            let l = t.parseProperty(s, i, e);
                            l && (n || (n = {}), n[a] = l)
                        }
                        return n
                    }
                    parseProperty(e, t) {
                        if (!e || !e.length) return;
                        const n = this;
                        let r, o = e.length,
                            i = 0,
                            s = 0,
                            a = 0,
                            l = !0;
                        for (; s < o;) {
                            i = e.indexOf("{{", s);
                            let t = e.indexOf("[[", s),
                                n = "}}";
                            if (t >= 0 && (i < 0 || t < i) && (i = t, l = !1, n = "]]"), a = i < 0 ? -1 : e.indexOf(n, i + 2), a < 0) return;
                            r = r || {};
                            let o = e.slice(i + 2, a).trim();
                            r.name = o, s = a + 2
                        }
                        const d = r.name,
                            c = n ? n._properties[d] : null;
                        return r.twoWay = l, r.ready = !1, n && (d.indexOf("::") >= 0 ? n.boundProperties[d.substring(0, d.indexOf("::"))] = !0 : n.boundProperties[d] = !0), c ? (r.type = c.type, r.reflectToAttribute = c.reflectToAttribute) : (["checked", "selected", "async", "autofocus", "autoplay", "controls", "defer", "disabled", "hidden", "ismap", "loop", "multiple", "open", "readonly", "required", "scoped"].indexOf(t) >= 0 ? r.type = "boolean" : r.type = "string", r.reflectToAttribute = !0), r
                    }
                    updateTextNodes() {
                        const e = this;
                        e.updateTextNode(e.shadowRoot || e, e.bindings, e)
                    }
                    updateTextNode(e, t, n) {
                        const r = this;
                        if (!t) return;
                        let o = 0;
                        for (let i = e.firstChild; i && t.children; i = i.nextSibling) r.updateTextNode(i, t.children[o++], n);
                        if (t && t.data)
                            for (let e in t.data) {
                                const r = t.data[e],
                                    o = r.name;
                                "textContent" === e && r.twoWay && !r.updating && void 0 !== r.value && (n[o] = r.value)
                            }
                    }
                    updateBoundProperty(e, t) {
                        if (t.updating) return;
                        const n = this;
                        t.updating = !0, n[e] = t.value, t.updating = !1
                    }
                    updateBoundNodes(e) {
                        const t = this;
                        if (t.updateBoundNode(t.shadowRoot || t, t.bindings, t, e), t.detachedChildren.length > 0)
                            for (let n = 0; n < t.detachedChildren.length; n++) {
                                const r = t.detachedChildren[n],
                                    o = r.getAttribute("smart-id"),
                                    i = function(e) { if (e.nodeId === o) return e; for (let t in e.children) { const n = e.children[t]; if ((n.getAttribute ? n.getAttribute("smart-id") : "") === o) return e; if (n.children) { const e = i(n); if (e) return e } } return null },
                                    s = i(t.bindings);
                                if (s) t.updateBoundNode(r, s, t, e, !0);
                                else if (r.getAttribute && t.bindings.mapping) {
                                    const n = t,
                                        r = t.bindings;
                                    if (r)
                                        for (let o in r.mapping) {
                                            const i = n.querySelector('[smart-id="' + o + '"]');
                                            if (i) {
                                                const s = r.mapping[o];
                                                t.updateBoundData(i, s, n, e)
                                            }
                                        }
                                }
                            }
                    }
                    updateBoundMappedNodes() {
                        const e = this,
                            t = e.bindings,
                            n = e;
                        if (t.mapping)
                            for (let r in t.mapping) {
                                let o = n.querySelector('[smart-id="' + r + '"]');
                                if (n.shadowRoot && (o = n.querySelector('[id="' + r + '"]'), o || (o = n.shadowRoot.querySelector('[id="' + r + '"]') || n.shadowRoot.querySelector('[smart-id="' + r + '"]'))), o) {
                                    const i = t.mapping[r];
                                    e.updateBoundData(o, i, n)
                                } else if (n.getAttribute("aria-controls")) {
                                    let i = document.getElementById(n.getAttribute("aria-controls"));
                                    if (!i && n.shadowRoot && (i = n.shadowRoot.getElementById(n.getAttribute("aria-controls"))), o = i.querySelector('[smart-id="' + r + '"]'), o) {
                                        const i = t.mapping[r];
                                        e.updateBoundData(o, i, n)
                                    }
                                }
                            }
                    }
                    updateBoundNode(e, t, n, r, o) {
                        const i = this;
                        if (!t) return;
                        let s = 0;
                        if (o) {
                            if (o && !t.data)
                                for (let a = e.firstChild; a && t.children; a = a.nextSibling)
                                    if (a.getAttribute) {
                                        const e = a.getAttribute("smart-id"),
                                            o = function() {
                                                for (let n in t.children)
                                                    if (t.children[n].nodeId === e) return t.children[n]
                                            }();
                                        i.updateBoundNode(a, o, n, r), s++
                                    } else i.updateBoundNode(a, t.children[s++], n, r, o)
                        } else
                            for (let o = e.firstChild; o && t.children; o = o.nextSibling)
                                if (o.getAttribute) {
                                    const e = o.getAttribute("smart-id"),
                                        a = function() {
                                            for (let n in t.children)
                                                if (t.children[n].nodeId === e) return t.children[n]
                                        }();
                                    i.updateBoundNode(o, a, n, r), s++
                                } else i.updateBoundNode(o, t.children[s++], n, r); if (!t || !t.data) return;
                        const a = t.data;
                        i.updateBoundData(e, a, n, r)
                    }
                    updateBoundData(e, t, n, r) {
                        const o = this;
                        for (let i in t) {
                            const s = t[i];
                            let a = s.name;
                            if (!s.updating && (a.indexOf("::") >= 0 && (a = a.substring(0, a.indexOf("::"))), void 0 === r || r === a)) {
                                if (a.indexOf("(") >= 0) {
                                    let e = a.substring(a.indexOf("("));
                                    const t = a.substring(0, a.indexOf("("));
                                    if (e = e.substring(1, e.length - 1), e = e.replace(/ /gi, ""), e = e.split(","), e.length > 0 && "" !== e[0]) {
                                        let r = [];
                                        for (let t = 0; t < e.length; t++) r.push(n[e[t]]);
                                        s.value = n[t].apply(n, r)
                                    } else s.value = n[t]();
                                    s.type = typeof s.value
                                } else s.value = n[a];
                                if ("innerHTML" === a) {
                                    if (e[i].toString().trim() !== n[a].toString().trim()) {
                                        if (window.smartBlazor && e[i].indexOf("\x3c!--") >= 0) {
                                            (s.ready || n._properties[a].defaultValue !== s.value) && (e[i] = s.value.toString());
                                            continue
                                        }(s.ready || n._properties[a].defaultValue !== s.value) && (e[i] = s.value.toString().trim())
                                    }
                                } else s.not ? (e[i] = !s.value, s.targetPropertyName && (e[s.targetPropertyName] = !s.value)) : (e[i] = s.value, s.targetPropertyName && (e[s.targetPropertyName] = s.value));
                                if (e.$ && e.$.isNativeElement) {
                                    v.cache["toDash" + i] || (v.cache["toDash" + i] = y.Core.toDash(i));
                                    const t = v.cache["toDash" + i],
                                        n = e.$.getAttributeValue(t, s.type);
                                    !s.reflectToAttribute || n === s.value && s.ready || e.$.setAttributeValue(t, s.value, s.type), s.reflectToAttribute || e.$.setAttributeValue(t, null, s.type)
                                }
                                if (!s.ready) {
                                    if (e.$ && e.$.isCustomElement) {
                                        v.cache["toDash" + i] || (v.cache["toDash" + i] = y.Core.toDash(i));
                                        const t = v.cache["toDash" + i];
                                        e._properties || (e._beforeCreatedProperties = e._properties = e.propertyByAttributeName = []), e._properties[i] || (e._properties[i] = { attributeName: t }, e._beforeCreatedProperties && (e._beforeCreatedProperties[i] = e._properties[i]), e.propertyByAttributeName[t] = e._properties[i]);
                                        const n = e._properties[i];
                                        n.isUpdating = !0, s.reflectToAttribute && (s.not ? e.$.setAttributeValue(n.attributeName, !s.value, s.type) : e.$.setAttributeValue(n.attributeName, s.value, s.type)), s.reflectToAttribute || e.$.setAttributeValue(n.attributeName, null, s.type), n.isUpdating = !1
                                    }
                                    if (s.twoWay) {
                                        const t = function(t) {
                                            if (s.value = t, e.$ && e.$.isNativeElement) {
                                                v.cache["toDash" + i] || (v.cache["toDash" + i] = y.Core.toDash(i));
                                                const t = v.cache["toDash" + i],
                                                    n = e.$.getAttributeValue(t, s.type);
                                                s.reflectToAttribute && n !== s.value && e.$.setAttributeValue(t, s.value, s.type), s.reflectToAttribute || e.$.setAttributeValue(t, null, s.type)
                                            }
                                        };
                                        if (s.name.indexOf("::") >= 0) {
                                            const n = s.name.indexOf("::"),
                                                r = s.name.substring(n + 2);
                                            o["$" + e.getAttribute("smart-id")].listen(r, (function() {
                                                t(e[i]);
                                                const n = s.name.substring(0, s.name.indexOf("::"));
                                                o.updateBoundProperty(n, s)
                                            }))
                                        }
                                        if (e.$ && e.$.isCustomElement) {
                                            e._properties[i] && (e._properties[i].notify = !0), v.cache["toDash" + i] || (v.cache["toDash" + i] = y.Core.toDash(i));
                                            const n = v.cache["toDash" + i];
                                            o["$" + e.getAttribute("smart-id")].listen(n + "-changed", (function(e) {
                                                let n = e.detail;
                                                t(n.value);
                                                const r = o.context;
                                                e.context !== document && (o.context = o), o.updateBoundProperty(s.name, s), o.context = r
                                            }))
                                        }
                                    }
                                }
                                s.ready = !0
                            }
                        }
                    }
                    static clearCache() { this.cache = {} }
                    addMessages(e, t) { Object.assign(this.messages[e], t) }
                    localize(e, t) {
                        const n = this;
                        if (!n.messages || !n.messages[n.locale]) return;
                        let r = n.messages[n.locale][e];
                        if ("" === r) return "";
                        if (!r) {
                            const r = n.messages.en;
                            if (r) {
                                let n = r[e];
                                if (n) {
                                    for (let e in t) {
                                        let r = t[e];
                                        n = n.replace(new RegExp("{{" + e + "}}", "g"), r)
                                    }
                                    return n
                                }
                                return e
                            }
                        }
                        const o = r;
                        for (let e in t) {
                            let n = t[e];
                            r = r.replace(new RegExp("{{" + e + "}}", "g"), n)
                        }
                        return n.localizeFormatFunction && n.localizeFormatFunction(o, r, t), r
                    }
                    static get requires() { return {} }
                    static get listeners() { return { "theme-changed": function(e) { this.theme = e.detail.newValue } } }
                    static get methods() { return {} }
                    get classNamesMap() { return { animation: "smart-animate", rippleAnimation: "smart-ripple" } }
                    get hasAnimation() { return "none" !== this.animation }
                    get hasRippleAnimation() { return "none" !== this.animation && "advanced" === this.animation }
                    static get modules() { return window[n].Modules }
                    get properties() { const e = this; return e._properties || (e._properties = []), e._properties }
                    get parents() {
                        const e = this;
                        let t = [],
                            r = e.parentNode;
                        for (; r && 9 !== r.nodeType;) r instanceof HTMLElement == 1 && t.push(r), r = r.parentNode;
                        const o = e.getRootNode();
                        if (o.host) {
                            const e = e => {
                                let t = [e],
                                    n = e.parentNode;
                                for (; n && 9 !== n.nodeType;) n instanceof HTMLElement == 1 && t.push(n), n = n.parentNode;
                                return t
                            };
                            t = t.concat(e(o.host))
                        }
                        return window[n].EnableShadowDOM && e.isInShadowDOM && e.shadowParent && (t = t.concat(e.shadowParent.parents)), t
                    }
                    log(e) { this._logger("log", e) }
                    warn(e) { this._logger("warn", e) }
                    error(e) { this._logger("error", e) }
                    _logger(e, t) {
                        if (this.debugMode) {
                            const n = t instanceof Error ? t.message : t.toString();
                            console[e](n)
                        }
                        if (this.rethrowError && "error" === e) throw t
                    }
                    get focused() { return this.contains(document.activeElement) }
                    template() { return "<div></div>" }
                    registered() {
                        const e = this;
                        e.onRegistered && e.onRegistered()
                    }
                    created() {
                        const e = this;
                        e.isReady = !1, e._initElement(e), e._setModuleState("created"), e.onCreated && e.onCreated()
                    }
                    completed() {
                        const e = this;
                        e.isCompleted = !0, e._onCompleted && e._onCompleted(), e.onCompleted && e.onCompleted()
                    }
                    whenReady(e) {
                        const t = this;
                        t.isCompleted ? e() : (t.whenReadyCallbacks || (t.whenReadyCallbacks = []), t.whenReadyCallbacks.push(e))
                    }
                    whenRendered(e) {
                        const t = this;
                        t.isRendered ? e() : (t.whenRenderedCallbacks || (t.whenRenderedCallbacks = []), t.whenRenderedCallbacks.push(e))
                    }
                    addThemeClass() { const e = this; "" !== e.theme && e.classList.add("smart-" + e.theme) }
                    addDefaultClass() {
                        const e = this;
                        e.classList.add(n.toLowerCase() + "-element"), e.classList.add(e.nodeName.toLowerCase())
                    }
                    _renderShadowRoot() { const e = this; if (e.shadowRoot) { e.$.root.classList.add(e.nodeName.toLowerCase()); for (let t = 0; t < e.attributes.length; t++) { const n = e.attributes[t]; "class" === n.name || "id" === n.name || "style" === n.name || "tabindex" === n.name || n.name.indexOf("aria") >= 0 || e.$.root.setAttribute(n.name, n.value) } for (let t = 0; t < e.classList.length; t++) { const n = e.classList[t]; "smart-element-init" !== n && "smart-element" !== n && "smart-hidden" !== n && "smart-visibility-hidden" !== n && e.$.root.classList.add(n) } } }
                    render() {
                        const e = this;
                        if (!e.isRendered && (e.isRendered = !0, e.isRendering = !1, e.context = document, e._renderShadowRoot(), e.whenRenderedCallbacks)) {
                            for (let t = 0; t < e.whenRenderedCallbacks.length; t++) e.whenRenderedCallbacks[t]();
                            e.whenRenderedCallbacks = []
                        }
                        e.onRender && e.onRender(), e.disabled && e.setAttribute("aria-disabled", !0), e.readonly && -1 !== ["checkbox", "combobox", "grid", "gridcell", "listbox", "radiogroup", "slider", "spinbutton", "textbox"].indexOf(e.getAttribute("role")) && e.setAttribute("aria-readonly", !0)
                    }
                    ready() {
                        const e = this;
                        if (e._setId(), e.addThemeClass(), e.addDefaultClass(), "collapsed" === e.visibility ? e.classList.add("smart-hidden") : "hidden" === e.visibility && e.classList.add("smart-visibility-hidden"), e.dataContext && e.applyDataContext(), e.onReady && e.onReady(), e.shadowRoot && Smart(e._selector)) {
                            if (Smart(e._selector).styleUrls) { const t = Smart(e._selector).styleUrls; for (let n = 0; n < t.length; n++) e.importStyle(t[n]) }
                            if (Smart(e._selector).styles) {
                                const t = document.createElement("style");
                                t.innerHTML = Smart(e._selector).styles, e.shadowRoot.insertBefore(t, e.shadowRoot.firstChild)
                            }
                        }
                        Smart(e._selector) && Smart(e._selector).ready && Smart(e._selector).ready()
                    }
                    _setId() {
                        const e = this;
                        if (!e.id) {
                            const t = e.elementName;
                            e.id = t.slice(0, 1).toLowerCase() + t.slice(1) + Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)
                        }
                    }
                    checkLicense() { const e = this; "Evaluation" === window[n].License && -1 === window.location.hostname.indexOf("htmlelements") && (e.logWatermark(), e.logLicense(), window[n].License = "") }
                    logWatermark() {
                        const e = document.createElement("a");
                        e.href = "https://www.htmlelements.com/", e.innerHTML = "https://www.htmlelements.com/", e.style.position = "absolute", e.style.right = "5px", e.style.bottom = "5px", e.style.color = "#fff", e.style.padding = "20px", e.style.borderRadius = "5px", e.style.background = "#0C3D78", e.style.cursor = "pointer", e.style.zIndex = "999999", e.style.display = "block", e.style.fontSize = "24px", e.style.textDecoration = "none", e.style.fontWeight = "bold", e.style.opacity = 0, e.style.transition = "opacity .35s ease-in-out", e.id = "watermark", document.getElementById("watermark") || setTimeout((() => { document.getElementById("watermark") || (document.body.appendChild(e), setTimeout((() => { e.style.opacity = 1 })), setTimeout((() => { e.style.opacity = 0, setTimeout((() => { e.parentNode.removeChild(e) }), 350) }), 6e3)) }), 1e3)
                    }
                    logLicense() { console.log("****************************************************************************************************************"), console.log("****************************************************************************************************************"), console.log("****************************************************************************************************************"), console.log("*jQWidgets License Key Not Found."), console.log("*This is an EVALUATION only Version, it is NOT Licensed for software projects intended for PRODUCTION."), console.log("*if you want to hide this message, please send an email to: sales@jqwidgets.com for a license."), console.log("****************************************************************************************************************"), console.log("****************************************************************************************************************"), console.log("****************************************************************************************************************") }
                    get _selector() { const e = this; return e.id ? "#" + e.id : e.classList.length > 0 ? "." + e.classList[0] : "" }
                    applyDataContext(e) {
                        const t = this;
                        let n = "string" == typeof t.dataContext ? window[t.dataContext] || document[t.dataContext] : t.dataContext;
                        if (e && (n = e, t.dataContext = e), n) {
                            if (!n._uid) {
                                n._uid = (Date.now().toString(36) + Math.random().toString(36).substr(2, 5)).toUpperCase(), n._properties = [];
                                for (let e in n) {
                                    const r = n[e];
                                    "function" != typeof r && "_properties" !== e && "_uid" !== e && (n._properties[e] = r, Object.defineProperty(n, e, {
                                        configurable: !1,
                                        enumerable: !0,
                                        get: () => n._properties[e],
                                        set(r) {
                                            const o = n._properties[e];
                                            n._properties[e] = r;
                                            let i = [];
                                            i[e] = { oldValue: o, value: r }, i.length++, t.updatingDataContext = !0, w.fireEvent("dataContextPropertyChanged", { dataContext: n, properties: i }, { bubbles: !1, cancelable: !0 }), t.updatingDataContext = !1
                                        }
                                    }))
                                }
                            }
                            if (t.dataContextProperties = t.parseAttributes(t), t.dataContextPropertiesMap = {}, t.dataContextListeners = {}, t.dataContextProperties) {
                                t.updatingDataContext = !0;
                                for (let e in t.dataContextProperties) {
                                    const r = t.dataContextProperties[e],
                                        o = r.name;
                                    if (r.propertyName = e, t.dataContextPropertiesMap[o] = e, v.cache["toDash" + e] || (v.cache["toDash" + e] = y.Core.toDash(o)), r.isEvent) {
                                        const e = r.value;
                                        t.dataContextListeners[o] && t.removeEventListener(o, t.dataContextListeners[o]), t.dataContextListeners[o] = function(t) { n[e](t) }, t.addEventListener(o, t.dataContextListeners[o])
                                    }
                                    if (o.indexOf(".") >= 0) {
                                        const r = o.split(".");
                                        let i = n[r[0]];
                                        for (let e = 1; e < r.length; e++) i = i[r[e]];
                                        void 0 !== i && (t[e] = i)
                                    } else t[e] = n[o]
                                }
                                t.dataContextPropertyChangedHandler = function(e) {
                                    const n = e.detail.properties;
                                    if (e.detail.dataContext === ("string" == typeof t.dataContext ? window[t.dataContext] || document[t.dataContext] : t.dataContext))
                                        for (let e in n) {
                                            const r = t.dataContextPropertiesMap[e],
                                                o = t.context;
                                            r && (t.context = document, t[r] = n[e].value, t.context = o)
                                        }
                                }, w.listen("dataContextPropertyChanged", t.dataContextPropertyChangedHandler), t.updatingDataContext = !1
                            } else t.dataContextProperties = null
                        } else {
                            t.dataContextProperties = null;
                            const e = function() {
                                ("string" == typeof t.dataContext ? window[t.dataContext] || document[t.dataContext] : t.dataContext) && (t.applyDataContext(), window.removeEventListener("load", e))
                            };
                            window.addEventListener("load", e)
                        }
                    }
                    updateDataContextProperty(e) {
                        const t = this,
                            n = "string" == typeof t.dataContext ? window[t.dataContext] || document[t.dataContext] : t.dataContext,
                            r = t.dataContextProperties[e];
                        if (!t.updatingDataContext && r.twoWay) {
                            const o = r.name;
                            if (o.indexOf(".") >= 0) {
                                const r = o.split(".");
                                let i = n[r[0]];
                                for (let e = 1; e < r.length; e++) i = i[r[e]];
                                void 0 !== i && (i = t[e], c[n._uid] && (c[n._uid][e] = i))
                            } else n[o] = t[e], c[n._uid] && (c[n._uid][e] = n[o])
                        }
                    }
                    static get version() { return window[n].Version }
                    initProperties() {
                        const e = this;
                        if (Smart(e._selector) && Smart(e._selector).properties && (e._initProperties = Smart(e._selector).properties), e.hasAttribute("props") && !e.props ? e._initProperties = window[e.getAttribute("props")] : e.props && (e._initProperties = e.props), e._initProperties) {
                            const t = Object.keys(e._initProperties);
                            for (let n = 0; n < t.length; n++) {
                                const r = t[n],
                                    o = e._initProperties[r];
                                if (o.constructor === Smart.ObservableArray || o instanceof Smart.ObservableArray) e[r] = o.toArray();
                                else if (o.constructor === Smart.DataAdapter || "smartDataAdapter" === o.constructor.name || "object" == typeof o && Smart.DataAdapter && o instanceof Smart.DataAdapter || o instanceof Smart.Observable || o.constructor === Smart.Observable || "object" != typeof o || y.Types.isArray(o) || o instanceof Date) {
                                    if (void 0 === e[r] && -1 === ["onReady", "onAttached", "onDetached", "onCreated", "onCompleted"].indexOf(r)) {
                                        const t = e.localize("propertyUnknownName", { name: r });
                                        e.log(t)
                                    }
                                    e[r] = o
                                } else if ("messages" !== r)
                                    if ("dataSourceMap" !== r) {
                                        if ("object" == typeof o) {
                                            const t = function(n, r) {
                                                const o = Object.keys(n);
                                                for (let i = 0; i < o.length; i++) {
                                                    const s = o[i],
                                                        a = n[s],
                                                        l = e._properties[r + "_" + s];
                                                    if (l && null === l.value) {
                                                        if (void 0 === e[r + "_" + s]) {
                                                            const t = e.localize("propertyUnknownName", { name: r + "_" + s });
                                                            e.log(t)
                                                        }
                                                        e[r + "_" + s] = a
                                                    } else if ("object" == typeof a && !y.Types.isArray(a) && a && a.constructor !== Date) t(a, r + "_" + s);
                                                    else {
                                                        if (void 0 === e[r + "_" + s]) {
                                                            const t = e.localize("propertyUnknownName", { name: r + "_" + s });
                                                            e.log(t)
                                                        }
                                                        e[r + "_" + s] = a
                                                    }
                                                }
                                            };
                                            t(o, r)
                                        }
                                    } else e[r] = o;
                                else e[r] = Object.assign(e[r], o)
                            }
                        }
                    }
                    setProperties(e) {
                        const t = this,
                            n = Object.keys(e);
                        for (let r = 0; r < n.length; r++) {
                            const o = n[r],
                                i = e[o];
                            if (i.constructor === Smart.ObservableArray || i instanceof Smart.ObservableArray) t[o] = i.toArray();
                            else if (i.constructor === Smart.DataAdapter || "smartDataAdapter" === i.constructor.name || "object" == typeof i && Smart.DataAdapter && i instanceof Smart.DataAdapter || i instanceof Smart.Observable || i.constructor === Smart.Observable || "object" != typeof i || y.Types.isArray(i) || i instanceof Date) { if (void 0 === t[o] && -1 === ["onReady", "onAttached", "onDetached", "onCreated", "onCompleted"].indexOf(o)) continue; const e = t._properties[o]; "int" === e.type || "number" === e.type && "string" == typeof subPropertyValue ? "int" === e.type ? t[o] = parseInt(i) : t[o] = parseFloat(i) : t[o] = i } else if ("messages" !== o && "dataSourceMap" !== o) {
                                if ("object" == typeof i) {
                                    const e = function(n, r) {
                                        const o = Object.keys(n);
                                        for (let i = 0; i < o.length; i++) {
                                            const s = o[i],
                                                a = n[s],
                                                l = t._properties[r + "_" + s];
                                            if (l && null === l.value) { if (void 0 === t[r + "_" + s]) continue; const e = t._properties[r + "_" + s]; "int" === e.type || "number" === e.type && "string" == typeof a ? "int" === e.type ? t[r + "_" + s] = parseInt(a) : t[r + "_" + s] = parseFloat(a) : t[r + "_" + s] = a } else if ("object" == typeof a && !y.Types.isArray(a) && a && a.constructor !== Date) e(a, r + "_" + s);
                                            else { if (void 0 === t[r + "_" + s]) continue; const e = t._properties[r + "_" + s]; "int" === e.type || "number" === e.type && "string" == typeof a ? "int" === e.type ? t[r + "_" + s] = parseInt(a) : t[r + "_" + s] = parseFloat(a) : t[r + "_" + s] = a }
                                        }
                                    };
                                    e(i, o)
                                }
                            } else t[o] = i
                        }
                    }
                    setup() {
                        const e = this;
                        if (e.context = this, e.isReady && !e.isCompleted) return;
                        if (e.isReady) return e._setModuleState("attached"), e.isAttached = !0, e.attached(), e._handleListeners("listen"), void(e.context = document);
                        e.ownerElement && e.ownerElement.detachedChildren.indexOf(e) >= 0 && e.ownerElement.detachedChildren.splice(e.ownerElement.detachedChildren.indexOf(e), 1), e.isReady = !0, e.methods = e.getStaticMember("methods"), e.initProperties(), a.isMobile && e.classList.add("smart-mobile");
                        for (let t = 0; t < e.attributes.length; t += 1) {
                            const n = e.propertyByAttributeName[e.attributes[t].name];
                            if (!n) continue;
                            let r = e.$.getAttributeValue(n.attributeName, n.type);
                            const o = r ? r.toString() : "";
                            if (!(o.indexOf("{{") >= 0 || o.indexOf("[[") >= 0 || "object" !== n.type && "array" !== n.type && (e.attributes[t].value.indexOf("{{") >= 0 || e.attributes[t].value.indexOf("[[") >= 0) || void 0 === r || n.value === r)) {
                                const o = y.Types.getType(r),
                                    i = e.attributes[t].value;
                                if (("any" === n.type || "object" === n.type) && "" + e[n.name] === r) continue;
                                if ("array" === n.type && e[n.name] && JSON.stringify(e[n.name]) === r) continue;
                                if ("number" === o && isNaN(r) && "NaN" !== i && "Infinity" !== i && "-Infinity" !== i) {
                                    const t = e.localize("propertyInvalidValueType", { name: n.name, actualType: "string", type: n.type });
                                    e.log(t)
                                }
                                n.isUpdatingFromAttribute = !0, e[n.name] = r, n.isUpdatingFromAttribute = !1
                            }
                        }
                        for (let t in e._properties) {
                            const n = e._properties[t];
                            if ("innerHTML" === t && n.value === n.defaultValue && (n.value = n.defaultValue = y.Core.html(e)), "boolean" !== n.type && "bool" !== n.type || "false" === e.getAttribute(n.attributeName) && (n.isUpdating = !0, e.setAttribute(n.attributeName, ""), n.isUpdating = !1), n.defaultReflectToAttribute && n.reflectToAttribute) {
                                if (n.defaultReflectToAttribute && n.defaultReflectToAttributeConditions) {
                                    let t = !0;
                                    for (let r = 0; r < n.defaultReflectToAttributeConditions.length; r++) {
                                        const o = n.defaultReflectToAttributeConditions[r];
                                        let i, s;
                                        for (let e in o) i = e, s = o[e];
                                        e._properties[i] && e._properties[i].value !== s && (t = !1)
                                    }
                                    if (!t) continue
                                }
                                n.isUpdating = !0, e.$.setAttributeValue(n.attributeName, n.value, n.type), n.isUpdating = !1
                            }
                        }
                        const t = [];
                        if (e.children.length > 0)
                            for (let n = 0; n < e.children.length; n++) {
                                const r = e.children[n];
                                y.Extend(r).isCustomElement && t.push(r)
                            }
                        e.applyTemplate(), e.complete = function() {
                            if (!e.templateBindingsReady) {
                                const t = e => { e.templateBindingsReady || (e.templateBindingsReady = !0, e.updateTextNodes(), e.updateBoundNodes()) };
                                if (e.ownerElement) {
                                    let n = e.ownerElement,
                                        r = [];
                                    for (; n;) r.push(n), n = n.ownerElement;
                                    for (let e = r.length - 1; e >= 0; e--) t(r[e]);
                                    t(e)
                                } else t(e)
                            }
                            const t = () => {
                                if (e._setModuleState("ready"), e.ready(), "auto" !== e.renderMode || e.isRendered || e.render(), e.isAttached = !0, e._setModuleState("attached"), e.attached(), e._handleListeners("listen"), e.isHidden || 0 !== e.offsetWidth && 0 !== e.offsetHeight || (e.isHidden = !0), e.completed(), e.isRendered && (e.context = document), e.whenReadyCallbacks) {
                                    for (let t = 0; t < e.whenReadyCallbacks.length; t++) e.whenReadyCallbacks[t]();
                                    e.whenReadyCallbacks = []
                                }
                            };
                            if (e.wait) e.classList.add("smart-visibility-hidden");
                            else if (e.classList.contains("smart-async")) requestAnimationFrame((() => { t() }));
                            else {
                                const n = e.shadowParent;
                                e.shadowParent = null;
                                const r = e.parents;
                                if (e.shadowParent = n, 0 === r.length) return;
                                const o = () => {
                                    let t = e.ownerElement,
                                        n = [];
                                    for (; t;) n.push(t), t = t.ownerElement;
                                    for (let e = n.length - 1; e >= 0; e--) n[e].updateBoundMappedNodes()
                                };
                                e.ownerElement && "HTML" !== r[r.length - 1].nodeName ? e.getRootNode().host ? t() : e.ownerElement && "HTML" === e.ownerElement.parents[e.ownerElement.parents.length - 1].nodeName ? (o(), t()) : e.checkIsInDomInterval = setInterval((() => { const n = e.parents; "HTML" === n[n.length - 1].nodeName && (clearInterval(e.checkIsInDomInterval), o(), t()) }), 100) : t()
                            }
                        };
                        let r = [].slice.call(e.querySelectorAll("[smart-id]")).concat(t);
                        if (window[n].EnableShadowDOM && !0 !== e.isInShadowDOM && (r = [].slice.call(e.shadowRoot.querySelectorAll("[smart-id]")).concat(t)), 0 === r.length) e.complete();
                        else {
                            e._completeListeners = 0;
                            for (let t = 0; t < r.length; t++) {
                                const n = r[t];
                                if (y.Extend(n).isCustomElement) {
                                    const t = function() { e._completeListeners--, 0 === e._completeListeners && (e.complete(), delete e._completeListeners) }.bind(e);
                                    n.isCompleted || n.isUtilityElement || !0 === n.wait || (e._completeListeners++, n._onCompleted || (n.completeHandlers = [], n._onCompleted = function() { for (let e = 0; e < n.completeHandlers.length; e++) n.completeHandlers[e]() }), n.completeHandlers.push(t))
                                }
                            }
                            0 === e._completeListeners && e.complete()
                        }
                    }
                    visibilityChangedHandler() {
                        const e = this;
                        e.isReady && requestAnimationFrame((() => { 0 === e.offsetWidth || 0 === e.offsetHeight ? e.isHidden = !0 : (e.isHidden = !1, e.$.fireEvent("resize", e, { bubbles: !1, cancelable: !0 })) }))
                    }
                    attributeChangedCallback(e, t, n) {
                        const r = this,
                            o = r.propertyByAttributeName[e];
                        if ("class" !== e && "style" !== e || r.visibilityChangedHandler(), o || r.attributeChanged(e, t, n), r.onAttributeChanged && r.onAttributeChanged(e, t, n), !o || o && o.isUpdating) return;
                        let i = r.$.getAttributeValue(o.attributeName, o.type);
                        void 0 !== n && r[o.name] !== i && (o.isUpdatingFromAttribute = !0, r[o.name] = void 0 !== i ? i : r._properties[o.name].defaultValue, o.isUpdatingFromAttribute = !1)
                    }
                    attributeChanged(e, t, n) {}
                    set hasStyleObserver(e) {
                        const t = this;
                        void 0 === t._hasStyleObserver && (t._hasStyleObserver = e), e ? d.watch(t) : d.unwatch(t)
                    }
                    get hasStyleObserver() { const e = this; return void 0 === e._hasStyleObserver || e._hasStyleObserver }
                    attached() {
                        const e = this;
                        e.hasStyleObserver && d.watch(e), e.onAttached && e.onAttached(), Smart(e._selector) && Smart(e._selector).attached && Smart(e._selector).attached()
                    }
                    detached() {
                        const e = this;
                        e.hasStyleObserver && d.unwatch(e), e._setModuleState("detached"), e.isAttached = !1, e.ownerElement && -1 === e.ownerElement.detachedChildren.indexOf(e) && e.ownerElement.detachedChildren.push(e), e._handleListeners("unlisten"), e.onDetached && e.onDetached(), Smart(e._selector) && Smart(e._selector).detached && Smart(e._selector).detached(), u && u[e._selector] && delete u[e._selector]
                    }
                    propertyChangedHandler(e, t, n) {
                        const r = this;
                        t !== n && ("theme" === e && ("" !== t && r.classList.remove("smart-" + t), "" !== n && r.classList.add("smart-" + n)), "visibility" === e ? ("collapsed" === t ? r.classList.remove("smart-hidden") : "hidden" === t && r.classList.remove("smart-visibility-hidden"), "collapsed" === n ? r.classList.add("smart-hidden") : "hidden" === n && r.classList.add("smart-visibility-hidden")) : ("disabled" === e || "readonly" === e) && r._ariaPropertyChangedHandler(e, n), r.propertyChanged && r.propertyChanged(e, t, n))
                    }
                    _ariaPropertyChangedHandler(e, t) { const n = this; "readonly" === e && -1 === ["checkbox", "combobox", "grid", "gridcell", "listbox", "radiogroup", "slider", "spinbutton", "textbox"].indexOf(n.getAttribute("role")) || (t ? n.setAttribute("aria-" + e, !0) : n.removeAttribute("aria-" + e)) }
                    _handleListeners(e) {
                        const t = this,
                            n = t.tagName.toLowerCase(),
                            r = r => {
                                for (let o in r) {
                                    const i = o.split(".");
                                    let s = i[0],
                                        a = t.$;
                                    if (i[1])
                                        if (s = i[1], a = t["$" + i[0]], "document" === i[0]) { let e = t.smartId; "" === e && (e = y.Core.toCamelCase(n)), s = s + "." + e } else t.smartId && (s = s + "." + t.smartId + "_" + t.parents.length);
                                    else t.smartId && (s = s + "." + t.smartId);
                                    const l = r[o],
                                        d = function(e) {
                                            const n = t.context;
                                            t.context = t, t[l] && t[l].apply(t, [e]), t.context = n
                                        };
                                    a && a[e](s, d)
                                }
                            };
                        r(t.getStaticMember("listeners")), r(t.templateListeners), Smart(t._selector) && Smart(t._selector).properties && r(Smart(t._selector).listeners)
                    }
                    parseTemplate() {
                        const e = this,
                            n = e.template(),
                            o = document.createDocumentFragment();
                        if (t[e.nodeName] && !r) return t[e.nodeName].cloneNode(!0);
                        if ("" === n) return null;
                        let i = document.createElement("div");
                        o.appendChild(i), i.innerHTML = n;
                        let s = i.childNodes;
                        i.parentNode.removeChild(i);
                        for (let e = 0; e < s.length; e++) o.appendChild(s[e]);
                        return t[e.nodeName] = o, r ? o : o.cloneNode(!0)
                    }
                    applyTemplate() {
                        const e = this,
                            t = e.parseTemplate();
                        if (!t) return;
                        if (!t.hasChildNodes) return;
                        const n = t.childNodes[0],
                            r = (t, n) => { e["$" + t] = n.$ = y.Extend(n), e.$[t] = n, n.ownerElement = e };
                        let o = n;
                        if (n.getElementsByTagName("content").length > 0) {
                            let e = n.getElementsByTagName("content")[0];
                            o = e.parentNode, o.removeChild(e)
                        } else {
                            const e = t.querySelectorAll("[inner-h-t-m-l]");
                            e && e.length > 0 && (o = e[0])
                        }
                        e.$.template = "template" === n.nodeName.toLowerCase() ? n : n.querySelector("template");
                        let i = t.querySelectorAll("[id]");
                        0 === i.length && (i = t.querySelectorAll("*")), r("root", n), r("content", o), e.$.html = e.innerHTML.toString().trim();
                        for (let t = 0; t < i.length; t += 1) { let n = i[t]; "" === n.id && (n.id = "child" + t), r(n.id, n), n.setAttribute("smart-id", n.id), e.shadowRoot ? n.shadowParent = e : n.removeAttribute("id") }
                        for (!1 !== e.hasTemplateBindings ? e.bindings = e.getBindings(t) : e.bindings = [], e.$root.addClass("smart-container"); e.childNodes.length;) o.appendChild(e.firstChild);
                        if (e.appendTemplate(t), e.$.template) {
                            const t = document.createElement("div");
                            t.classList.add("smart-template-container"), e.$.templateContainer = t, e.$.template.parentNode.insertBefore(t, e.$.template), e.refreshTemplate()
                        }
                    }
                    refreshTemplate() {
                        const e = this;
                        if (!e.$.templateContainer) return;
                        e.templateDetached(e.$.templateContainer);
                        const t = e.$.template.content.cloneNode(!0);
                        e.templateBindings = e.getBindings(t), e.templateProperties = [];
                        let n = document.createDocumentFragment();
                        const r = function(t, n, o) {
                            for (let i in t) {
                                const s = t[i],
                                    a = s.node.cloneNode();
                                n.appendChild(a);
                                let l = [],
                                    d = !1;
                                if (s.data)
                                    for (let t in s.data) {
                                        const r = s.data[t],
                                            i = r.name;
                                        if (e.templateProperties[i] = !0, a.removeAttribute(y.Core.toDash(t)), "*items" === t) l = e[i], d = !0;
                                        else if (i.indexOf("item.") >= 0 && void 0 !== o) r.value = o[i.substring("item.".length)], a[t] = r.value;
                                        else if (i.indexOf("item") >= 0 && void 0 !== o) r.value = o, a[t] = r.value;
                                        else if ("*if" === t)
                                            if (i.indexOf("(") >= 0) {
                                                let t, r = i.substring(i.indexOf("("));
                                                const o = i.substring(0, i.indexOf("("));
                                                if (r = r.substring(1, r.length - 1), r = r.replace(/ /gi, ""), r = r.split(","), r.length > 0 && "" !== r[0]) {
                                                    let n = [];
                                                    for (let t = 0; t < r.length; t++) n.push(e[r[t]]);
                                                    t = e[o].apply(e, n)
                                                } else t = e[o]();
                                                !1 === t && n.removeChild(a)
                                            } else e[i] || n.removeChild(a);
                                        else e.updateBoundNode(a, s, e, i)
                                    }
                                if (l.length > 0 || d) {
                                    for (let e = 0; e < l.length; e++) s.children && r(s.children, a, l[e]);
                                    if ("number" == typeof l)
                                        for (let e = 0; e < l; e++) s.children && r(s.children, a, e)
                                } else s.children && r(s.children, a, o)
                            }
                        };
                        r(e.templateBindings.children, n), e.$.templateContainer.innerHTML = "", e.$.templateContainer.appendChild(n), e.templateAttached(e.$.templateContainer)
                    }
                    templateAttached() {}
                    templateDetached() {}
                    appendTemplate(e) { this.appendChild(e) }
                    defineElementModules() {
                        const e = this,
                            t = e.constructor.prototype;
                        if ("BaseElement" === t.elementName) { t.modules = e.constructor.modules; const n = t.modules; for (let t = 0; t < n.length; t += 1) e.addModule(n[t]) } else {
                            const n = t.modules;
                            if (!n) return;
                            for (let t = 0; t < n.length; t += 1) {
                                const r = n[t],
                                    o = r.prototype;
                                e.defineElementMethods(o.methodNames, o), e.defineElementProperties(r.properties)
                            }
                        }
                    }
                    watch(e, t) {
                        const n = this;
                        n._watch = null !== e && null !== t ? { properties: e, propertyChangedCallback: t } : null
                    }
                    unwatch() { this._watch = null }
                    set(e, t, n) {
                        const r = this,
                            o = r.context;
                        r.context = !0 === n ? document : r, r[e] = t, r.context = o
                    }
                    get(e) { return this[e] }
                    _setModuleState(e, t) {
                        const n = this,
                            r = "is" + e.substring(0, 1).toUpperCase() + e.substring(1),
                            o = "on" + e.substring(0, 1).toUpperCase() + e.substring(1);
                        for (let i = 0; i < n.modulesList.length; i++) {
                            const s = n.modulesList[i];
                            s[r] = !0, s[e] && s[e](t), s[o] && s[o](t)
                        }
                    }
                    addModule(e, t) {
                        const n = this;
                        if (!e) return;
                        const r = n.modules.slice(0),
                            o = e.prototype,
                            i = Object.getPrototypeOf(e);
                        if (i.name && i.name !== e.name && n.addModule(i), !e.moduleName && e.name && (e.moduleName = e.name), -1 === r.findIndex((t => e.moduleName === t.moduleName)) && r.push(e), n.defineModule(e), n.defineElementMethods(o.methodNames, o), n.defineElementProperties(e.properties), n.constructor.prototype.modules = r, t)
                            for (let t in Smart.Elements.tagNames) {
                                const r = Smart.Elements.tagNames[t];
                                let o = Object.getPrototypeOf(r),
                                    i = [];
                                for (; o !== HTMLElement;) i.push(o.prototype), o = Object.getPrototypeOf(o);
                                i.indexOf(n) >= 0 && r !== n && r.prototype.addModule(e)
                            }
                    }
                    defineModule(e) {
                        if (e.isDefined) return;
                        e.prototype._initModule = function(e) { this.ownerElement = e };
                        const t = e.properties || {},
                            n = Object.keys(t),
                            r = Object.getOwnPropertyNames(e.prototype);
                        e.prototype.methodNames = r;
                        for (let r = 0; r < n.length; r += 1) {
                            const o = n[r],
                                i = t[o];
                            Object.defineProperty(e.prototype, o, { configurable: !1, enumerable: !0, get() { return this.ownerElement ? this.ownerElement[o] : i.value }, set(e) { this.ownerElement[o] = e } })
                        }
                        e.isDefined = !0
                    }
                    getStaticMember(e, t) {
                        const r = window[n][this.elementName],
                            o = r[e];
                        t || (t = "");
                        let i = "array" === t ? [] : "string" === t ? "" : {},
                            s = Object.getPrototypeOf(r),
                            a = [];
                        for (; s[e];) a.push(s[e]), s = Object.getPrototypeOf(s);
                        for (let e = a.length - 1; e >= 0; e--)
                            if ("array" === t)
                                for (let t = 0; t < a[e].length; t++) - 1 === i.indexOf(a[e][t]) && i.push(a[e][t]);
                            else "string" === t ? -1 === i.indexOf(a[e]) && (i += a[e]) : i = y.Core.assign(i, a[e]);
                        if ("array" === t) { for (let e = 0; e < o.length; e++) - 1 === i.indexOf(o[e]) && i.push(o[e]); return i }
                        return "string" === t ? (-1 === i.indexOf(o) && (i += o), i) : y.Core.assign(i, o)
                    }
                    defineElementHierarchicalProperties(e, t) {
                        const n = this,
                            r = [];
                        ! function(e) {
                            const n = Object.keys(e);
                            for (let o = 0; o < n.length; o++) {
                                const i = n[o];
                                if ("messages" === i) continue;
                                const s = e[i],
                                    a = Object.keys(s),
                                    l = a.indexOf("value") >= 0 && a.indexOf("type") >= 0 && "object" == typeof s.value;
                                if ("propertyObject" === s.type || l) {
                                    const e = function(n, o) {
                                        if (!n.value) return;
                                        const i = Object.keys(n.value);
                                        for (let s = 0; s < i.length; s++) {
                                            const a = i[s],
                                                l = n.value[a],
                                                d = o + "_" + a;
                                            if ("object" != typeof l || null === l) break;
                                            const c = Object.keys(l);
                                            if (!(c.indexOf("value") >= 0 && c.indexOf("type") >= 0)) break;
                                            if ("array" !== n.type && (n.isHierarchicalProperty = !0), l.parentPropertyName = o, t) {
                                                const e = t._properties[d];
                                                if (n.value.hasOwnProperty(a)) {
                                                    if (e.isDefined) continue;
                                                    delete n.value[a]
                                                }
                                                e.isDefined = !0, Object.defineProperty(n.value, a, { configurable: !1, enumerable: !0, get: () => t._properties[d].value, set(e) { t.updateProperty(t, t._properties[d], e) } })
                                            }
                                            r[d] || (r[d] = l, r.length++), ("propertyObject" === l.type || "object" == typeof l.value && "array" !== l.type) && e(t ? t._properties[d] : l, d)
                                        }
                                    };
                                    e(s, i)
                                }
                            }
                        }(e), r.length > 0 && !t && n.defineElementProperties(r)
                    }
                    defineElement() {
                        const e = this,
                            t = e.constructor.prototype,
                            n = e.getStaticMember("properties"),
                            r = Object.getOwnPropertyNames(t);
                        t.extendedProperties = {}, t.boundProperties = {}, t.templateListeners = {}, e.defineElementModules(), e.defineElementMethods(r, t), e.defineElementProperties(n), e.defineElementHierarchicalProperties(e.extendedProperties), t._initElement = function() {
                            const e = this,
                                n = t.extendedProperties,
                                r = Object.keys(n),
                                o = e.modules;
                            e.$ = y.Extend(e), e.$document = w, e.smartId = (Date.now().toString(36) + Math.random().toString(36).substr(2, 5)).toUpperCase(), e.isCreated || (e.modulesList = [], e._properties = [], e._beforeCreatedProperties && (e._properties = e._beforeCreatedProperties, delete e._beforeCreatedProperties), e.detachedChildren = [], e.propertyByAttributeName = []);
                            for (let t = 0; t < o.length; t += 1) {
                                let n = new(0, o[t]);
                                n._initModule(e), e.modulesList.push(n)
                            }
                            for (let t = 0; t < r.length; t += 1) {
                                const o = r[t],
                                    i = n[o];
                                let s = i.value;
                                if (e._properties[o]) {
                                    if (void 0 !== e._properties[o].notify) continue;
                                    delete e._properties[o]
                                }
                                if (E && "innerHTML" === o && delete e[o], -1 === window.navigator.userAgent.indexOf("PhantomJS") && e.hasOwnProperty(o) && (s = e[o], delete e[o]), "array" === i.type && null != s && (s = s.slice(0)), "object" === i.type && null != s && (s = Array.isArray(s) ? s.slice(0) : Object.assign({}, s)), e._properties[o] = { name: o, notify: i.notify, allowedValues: i.allowedValues, type: i.type, nullable: i.nullable, reflectToAttribute: i.reflectToAttribute, defaultReflectToAttribute: i.defaultReflectToAttribute, defaultReflectToAttributeConditions: i.defaultReflectToAttributeConditions, value: s, readOnly: i.readOnly, defaultValue: s, attributeName: i.attributeName, observer: i.observer, inherit: i.inherit, extend: i.extend, validator: i.validator }, e.propertyByAttributeName[i.attributeName] = e._properties[o], !i.hasOwnProperty("type")) {
                                    const t = e.localize("propertyUnknownType", { name: o });
                                    e.log(t)
                                }
                                if ("any" === i.type || "propertyObject" === i.type) continue;
                                const a = y.Types.getType(s);
                                if (null != s && i.type !== a && !i.validator) {
                                    if ("object" === i.type && "array" === a) continue;
                                    if ("number" === a && ["integer", "int", "float"].findIndex((e => e === i.type)) >= 0) continue;
                                    const t = e.localize("propertyInvalidValueType", { name: o, actualType: a, type: i.type });
                                    e.log(t)
                                }
                            }
                            e.defineElementHierarchicalProperties(e._properties, e), e.isCreated = !0
                        }, t.registered()
                    }
                    defineElementMethods(e, t) {
                        const n = this.constructor.prototype,
                            r = function(e, t) {
                                const n = Array.prototype.slice.call(arguments, 2),
                                    r = function() {
                                        if (!this.isReady && "localize" !== t && "localize" !== t && "cloneNode" !== t && "importStyle" !== t && "log" !== t && "parseAttributes" !== t) {
                                            const e = this.localize("elementNotInDOM");
                                            this.log(e)
                                        }
                                        let r = this;
                                        for (let e = 0; e < this.modulesList.length; e++) { let n = this.modulesList[e]; if (t in n) { r = n; break } }
                                        const o = this.context,
                                            i = n.concat(Array.prototype.slice.call(arguments));
                                        let s = null;
                                        const a = function(e, t) { return e === t || "number" === e && ("int" === t || "integer" === t || "float" === t) || "bool" === e && "boolean" === t || "boolean" === e && "bool" === t || "object" === e && "any" === t || void 0 };
                                        if (this.methods) {
                                            const e = this.methods[t];
                                            if (e) {
                                                const n = e.split(":");
                                                s = n[n.length - 1].trim();
                                                const r = [],
                                                    o = e.substring(1 + e.indexOf("("), e.lastIndexOf(")")).split(",");
                                                let l = "";
                                                for (let e = 0; e < o.length; e++) {
                                                    const t = o[e];
                                                    l += t, t.indexOf(":") >= 0 ? (r.push(l), l = "") : l += ","
                                                }
                                                let d = r.length;
                                                for (let e = 0; e < r.length; e++) {
                                                    const n = r[e].trim().split(":"),
                                                        o = n[0].split("=")[0].trim().indexOf("?") >= 0,
                                                        s = n[1].indexOf("?") >= 0,
                                                        l = n[1].replace(/\?/gi, "").trim(),
                                                        c = l.split("|");
                                                    let u = n[0].split("=")[1];
                                                    const p = y.Types.getType(i[e]);
                                                    if (void 0 === i[e] && u) {
                                                        switch (u = u.trim(), l[0]) {
                                                            case "date":
                                                                { let e = u.substring(u.indexOf("(") + 1, u.lastIndexOf(")"));e = e.length > 0 ? e.split(",").map((e => parseInt(e))) : [], u = 0 === e.length ? new Date : new Date(e[0], e[1], e[2]); break }
                                                            case "bool":
                                                            case "boolean":
                                                                u = "true" === u || "1" === u;
                                                                break;
                                                            case "int":
                                                            case "integer":
                                                                u = parseInt(u);
                                                                break;
                                                            case "float":
                                                            case "number":
                                                                u = parseFloat(u);
                                                                break;
                                                            case "any":
                                                            case "object":
                                                                u = u.indexOf("{") >= 0 ? JSON.parse(u) : u
                                                        }
                                                        i.push(u)
                                                    } else o && d--;
                                                    if (l !== p && p) {
                                                        let n = !0;
                                                        for (let e = 0; e < c.length; e++)
                                                            if (a(p, c[e])) { n = !1; break }
                                                        if (n && (null !== i[e] || !s)) {
                                                            const n = this.localize("methodInvalidValueType", { name: t, actualType: p, type: l, argumentIndex: e });
                                                            this.log(n)
                                                        }
                                                    }
                                                    if (i.length < d) {
                                                        const e = this.localize("methodInvalidArgumentsCount", { name: t, actualArgumentsCount: i.length, argumentsCount: d });
                                                        this.log(e)
                                                    }
                                                }
                                            }
                                        }
                                        this.context = this;
                                        const l = e.apply(r, i);
                                        if (s) {
                                            const e = void 0 === y.Types.getType(l) ? "void" : y.Types.getType(l);
                                            if (!a(e, s)) {
                                                const n = this.localize("methodInvalidReturnType", { name: t, actualType: e, type: s });
                                                this.log(n)
                                            }
                                        }
                                        return this.context = o, l
                                    };
                                return r
                            },
                            o = ["constructor", "ready", "created", "render", "attached", "detached", "appendChild", "insertBefore", "removeChild", "connect", "disconnectedCallback", "connectedCallback", "attributeChangedCallback", "propertyChangedHandler", "enableShadowDOM", "isInShadowDOM", "addPropertyBindings"];
                        for (let i in e) {
                            let s = e[i];
                            s && s.startsWith && s.startsWith("_") || void 0 !== o.find((e => e === s)) || n.extendedProperties[s] || y.Types.isFunction(t[s]) && (n[s] = r(t[s], s))
                        }
                    }
                    defineElementProperties(e) {
                        if (!e) return;
                        const t = this,
                            n = t.constructor.prototype,
                            r = Object.keys(e),
                            o = t.getStaticMember("properties");
                        Object.assign(n.extendedProperties, e), t.updateProperty = function(e, t, n) {
                            const r = e;
                            if (!t || t.readOnly) return;
                            if (t.allowedValues) {
                                let e = !1;
                                for (let r = 0; r < t.allowedValues.length; r++)
                                    if (t.allowedValues[r] === n) { e = !0; break }
                                if (!e) {
                                    const e = JSON.stringify(t.allowedValues).replace(/\[|\]/gi, "").replace(",", ", ").replace(/"/gi, "'"),
                                        o = "'" + n + "'",
                                        i = r.localize("propertyInvalidValue", { name: t.name, actualValue: o, value: e });
                                    return void r.log(i)
                                }
                            }
                            const o = t.name,
                                i = r._properties[o].value;
                            if (t.validator && r[t.validator]) {
                                const e = r.context;
                                r.context = r;
                                const o = r[t.validator](i, n);
                                void 0 !== o && (n = o), r.context = e
                            }
                            if (i !== n) {
                                if (r.propertyChanging) { const e = r.propertyChanging(o, i, n); if (!1 === e || null === e) return }
                                if (!t.hasOwnProperty("type")) {
                                    const e = r.localize("propertyUnknownType", { name: o });
                                    r.log(e)
                                }
                                if ("array" !== t.type || JSON.stringify(i) !== JSON.stringify(n)) {
                                    if (null != n && "any" !== t.type && "propertyObject" !== t.type && t.type !== y.Types.getType(n) && !t.validator || null === n && !t.nullable) { let e = !0; if ("object" === t.type && "array" === y.Types.getType(n) && (e = !1), "number" === y.Types.getType(n) && ["integer", "int", "float"].findIndex((e => e === t.type)) >= 0 && (e = !1), e) { const e = r.localize("propertyInvalidValueType", { name: o, actualType: y.Types.getType(n), type: t.type }); return void r.error(e) } }
                                    if (t.isUpdating = !0, t.isHierarchicalProperty) {
                                        const e = function(t, n) {
                                            const o = Object.keys(t);
                                            for (let i = 0; i < o.length; i++) {
                                                const s = o[i],
                                                    a = t[s];
                                                "object" == typeof a && !y.Types.isArray(a) && a && a.constructor !== Date ? e(a, n + "_" + s) : r[n + "_" + s] = a
                                            }
                                        };
                                        e(n, o)
                                    } else r._properties[o].value = n;
                                    if (!t.isUpdatingFromAttribute && t.reflectToAttribute && r.$.setAttributeValue(t.attributeName, n, t.type), r.isReady && (!r.ownerElement || r.ownerElement && r.ownerElement.isReady)) {
                                        if ("wait" === o && (n || !i || r.isCompleted || (r.classList.remove("smart-visibility-hidden"), r.ownerElement && r.ownerElement.updateBoundMappedNodes(), r.updateBoundMappedNodes(), r.complete())), "renderMode" === o) return;
                                        if (r.context !== r && !r.wait) {
                                            const e = r.context;
                                            r.context = r, r.propertyChangedHandler(o, i, n), r.context = e, t.observer && r[t.observer] && (r.context = r, r[t.observer](i, n), r.context = document), r._watch && r._watch.properties.indexOf(o) >= 0 && r._watch.propertyChangedCallback(o, i, n)
                                        }
                                        const e = t.notify || r.boundProperties[o];
                                        e && (r.$.fireEvent(t.attributeName + "-changed", { context: r.context, oldValue: i, value: r[o] }), r.boundProperties[o] && r.updateBoundNodes(o)), e && r.templateProperties && r.templateProperties[o] && r.refreshTemplate(), r.dataContextProperties && ("dataContext" === o ? r.applyDataContext() : r.dataContextProperties[o] && r.updateDataContextProperty(o))
                                    }
                                    t.isUpdating = !1
                                }
                            }
                        };
                        for (let t = 0; t < r.length; t += 1) {
                            const i = r[t],
                                s = e[i],
                                a = y.Core.toDash(i),
                                l = s.type || "any",
                                d = l.indexOf("?") >= 0 || "any" === l;
                            d && "any" !== l && (s.type = l.substring(0, l.length - 1)), s.nullable = d, s.attributeName = a.toLowerCase(), s.name = i, s.reflectToAttribute = void 0 === s.reflectToAttribute || s.reflectToAttribute, s.inherit && o[i] && (s.value = o[i].value), s.extend && o[i] && y.Core.assign(s.value, o[i].value), n.hasOwnProperty(i) || Object.defineProperty(n, i, {
                                configurable: !1,
                                enumerable: !0,
                                get() { if (this._properties[i]) return this._properties[i].value },
                                set(e) {
                                    const t = this;
                                    t.updateProperty(t, t._properties[i], e)
                                }
                            })
                        }
                    }
                }
                let C = [],
                    S = [],
                    x = [],
                    E = !1;
                const A = navigator.userAgent.match(/Chrom(e|ium)\/([0-9]+)\./);
                A && parseInt(A[2], 10) <= 50 && (E = !0);
                class T {
                    static register(e, t) {
                        const r = t.prototype;
                        let o = a.toCamelCase(e).replace(/[a-z]+/, ""),
                            i = t.version || window[n].Version;
                        if (window.customElements.get(e) && window.customElements.get(e).version === i) return;
                        let s = e;
                        for (i = i.split("."); window.customElements.get(e);) e = s + "-" + i.join("."), i[2] = parseInt(i[2]) + 1;
                        if (!C[e]) {
                            if (e.startsWith(n.toLowerCase())) C[e] = window[n][o] = window[n.toLowerCase() + o] = t;
                            else {
                                let r = e.split("-")[0];
                                r = r.substring(0, 1).toUpperCase() + r.substring(1), window[n][r] || (window[n][r] = {}), C[e] = window[n][r][o] = window[r.toLowerCase() + o] = t, window[n][o] && (o = a.toCamelCase(e)), window[n][o] = t
                            }
                            r.elementName = o, r.defineElement(), S[e] && S[e](r), window.customElements.define(e, t)
                        }
                    }
                    static registerElements() {
                        const e = this;
                        if (e.toRegister) {
                            e.isRegistering = !0;
                            for (let t = 0; t < e.toRegister.length; t++) {
                                const n = e.toRegister[t];
                                e.register(n.tagName, n.element)
                            }
                            e.isRegistering = !1
                        }
                    }
                    static get(e) { if (C[e]) return C[e] }
                    static whenRegistered(e, t) {
                        if (!e) throw new Error("Syntax Error: Invalid tag name");
                        const n = S[e],
                            r = this.get(e),
                            o = r ? r.modules.length : 3;
                        try {
                            n || r ? !n && r ? (t(r.prototype), S[e] = void 0) : n && !r ? S[e] = function(e) { n(e), t(e) } : n && r && (r.proto && (n(r.proto), t(r.proto)), S[e] = void 0) : S[e] = function(e) {
                                try { t(e) } catch (e) {
                                    const t = e instanceof Error ? e.message : e.toString();
                                    console.log(t)
                                }
                            }
                        } catch (e) {
                            const t = e instanceof Error ? e.message : e.toString();
                            console.log(t)
                        }
                        if (r && o !== r.prototype.modules.length) {
                            const t = document.querySelectorAll(e);
                            for (let e = 0; e < t.length; e++) {
                                const n = t[e];
                                n.isCreated && n._initElement()
                            }
                        }
                    }
                }
                T.lazyRegister = !1, T.tagNames = [];
                class P {
                    constructor() {
                        const e = this;
                        e.name = "observableArray", e.observables = arguments.length < 3 ? null : arguments[2];
                        const t = new Proxy(e, { deleteProperty: function(e, t) { return delete e[t], !0 }, apply: function(e, t, n) { return e.apply(t, n) }, get: function(t, n) { return t[n] || isNaN(parseInt(n)) ? t[n] : e.getItem(parseInt(n)) }, set: function(t, n, r) { return t[n] || isNaN(parseInt(n)) ? (t[n] = r, !0) : (e.setItem(parseInt(n), r), !0) } });
                        if (e._addArgs = { eventName: "change", object: t, action: "add", index: null, removed: new Array, addedCount: 1 }, e._removeArgs = { eventName: "change", object: t, action: "remove", index: null, removed: null, addedCount: 0 }, arguments.length >= 1 && Array.isArray(arguments[0])) {
                            e._array = [];
                            const t = arguments[0];
                            for (let n = 0, r = t.length; n < r; n++) {
                                const r = e._getItem(e._array.length, t[n]);
                                e._array.push(r)
                            }
                        } else e._array = Array.apply(null, arguments);
                        return 2 === arguments.length && (e.notifyFn = arguments[1]), t
                    }
                    get canNotify() { const e = this; return void 0 === e._canNotify && (e._canNotify = !0), e._canNotify }
                    set canNotify(e) { this._canNotify = e }
                    _notify(e) {
                        const t = this;
                        t.canNotify && t.notifyFn && t.notifyFn(e)
                    }
                    notify(e) { e && (this.notifyFn = e) }
                    toArray() { return this._array }
                    _getItem(e, t) { const n = this; return "string" == typeof t || "number" == typeof t || void 0 === t ? t : new Proxy(t, { deleteProperty: function(e, t) { return delete e[t], !0 }, set: function(t, r, o) { const i = t[r]; return t[r] = o, !n._canNotify || !1 === t.canNotify || (n.observables && !n.observables[r] || n._notify({ eventName: "change", object: n, target: t, action: "update", index: e, path: e + "." + r, oldValue: i, newValue: o, propertyName: r }), !0) } }) }
                    getItem(e) { return this._array[e] }
                    setItem(e, t) {
                        const n = this,
                            r = n._array[e];
                        n._array[e] = n._getItem(e, t), n._notify({ eventName: "change", object: n._array, action: "update", index: e, removed: [r], addedCount: 1 })
                    }
                    get length() { return this._array.length }
                    set length(e) {
                        const t = this;
                        o.isNumber(e) && t._array && t._array.length !== e && t.splice(e, t._array.length - e)
                    }
                    toString() { return this._array.toString() }
                    toLocaleString() { return this._array.toLocaleString() }
                    concat() {
                        const e = this;
                        e._addArgs.index = e._array.length;
                        const t = e._array.concat.apply(e._array, arguments);
                        return new Smart.ObservableArray(t)
                    }
                    join(e) { return this._array.join(e) }
                    pop() {
                        const e = this;
                        e._removeArgs.index = e._array.length - 1, delete e[e._array.length - 1];
                        const t = e._array.pop();
                        return e._removeArgs.removed = [t], e._notify(e._removeArgs), e._notifyLengthChange(), t
                    }
                    push() {
                        const e = this;
                        if (e._addArgs.index = e._array.length, 1 === arguments.length && Array.isArray(arguments[0])) {
                            const t = arguments[0];
                            for (let n = 0, r = t.length; n < r; n++) {
                                const r = e._getItem(e._array.length, t[n]);
                                e._array.push(r)
                            }
                        } else {
                            const t = e._getItem(e._addArgs.index, arguments[0]);
                            e._array.push.apply(e._array, [t])
                        }
                        return e._addArgs.addedCount = e._array.length - e._addArgs.index, e._notify(e._addArgs), e._notifyLengthChange(), e._array.length
                    }
                    _notifyLengthChange() {
                        const e = this;
                        if (!e.canNotify) return;
                        const t = e._createPropertyChangeData("length", e._array.length);
                        e._notify(t)
                    }
                    _createPropertyChangeData(e, t, n) { return { eventName: "change", object: this, action: e, value: t, oldValue: n } }
                    reverse() { return this._array.reverse() }
                    shift() {
                        const e = this,
                            t = e._array.shift();
                        return e._removeArgs.index = 0, e._removeArgs.removed = [t], e._notify(e._removeArgs), e._notifyLengthChange(), t
                    }
                    slice(e, t) { return this._array.slice(e, t) }
                    sort(e) { return this._array.sort(e) }
                    splice(e, t, n) {
                        const r = this,
                            o = r._array.length;
                        let i;
                        if (n && n.length)
                            for (let o = 0; o < n.length; o++) i = r._array.splice(e + o, t, n[o]);
                        else i = r._array.splice.apply(r._array, arguments);
                        if (n) {
                            let t = r.canNotify;
                            if (r.canNotify = !1, n.length)
                                for (let t = 0; t < n.length; t++) r.setItem(e + t, n[t]);
                            else r.setItem(e, n);
                            r.canNotify = t, r._notify({ eventName: "change", object: this, action: "add", index: e, added: i, addedCount: r._array.length > o ? r._array.length - o : 0 })
                        } else r._notify({ eventName: "change", object: this, action: "remove", index: e, removed: i, addedCount: r._array.length > o ? r._array.length - o : 0 });
                        return r._array.length !== o && r._notifyLengthChange(), i
                    }
                    unshift() {
                        const e = this,
                            t = e._array.length,
                            n = e._array.unshift.apply(e._array, arguments);
                        return e._addArgs.index = 0, e._addArgs.addedCount = n - t, e._notify(this._addArgs), e._notifyLengthChange(), n
                    }
                    indexOf(e, t) {
                        const n = this;
                        for (let r = t || 0, o = n._array.length; r < o; r++)
                            if (n._array[r] === e) return r;
                        return -1
                    }
                    lastIndexOf(e, t) {
                        const n = this;
                        for (let r = t || n._array.length - 1; r >= 0; r--)
                            if (n._array[r] === e) return r;
                        return -1
                    }
                    find(e, t) { return this._array.find(e, t) }
                    findIndex(e, t) { return this._array.findIndex(e, t) }
                    every(e, t) { return this._array.every(e, t) }
                    some(e, t) { return this._array.some(e, t) }
                    forEach(e, t) { this._array.forEach(e, t) }
                    map(e, t) { return this._array.map(e, t) }
                    filter(e, t) { return this._array.filter(e, t) }
                    reduce(e, t) { return void 0 !== t ? this._array.reduce(e, t) : this._array.reduce(e) }
                    reduceRight(e, t) { return void 0 !== t ? this._array.reduceRight(e, t) : this._array.reduceRight(e) }
                    move(e, t) { this.splice(t, 0, this.splice(e, 1)[0]) }
                }
                let D = {};
                window[n] && (D = window[n]), window[n] = function(e, t) {
                    let r = e;
                    if (e) {
                        if (e.indexOf("#") >= 0 || e.indexOf(".") >= 0) return u[e] ? u[e] : t ? (u[e] = new t, function(e, t) {
                            const n = t.properties;
                            t._properties = [];
                            const r = function(n, o) {
                                const i = Object.keys(n);
                                for (let s = 0; s < i.length; s++) {
                                    const a = i[s],
                                        l = n[a];
                                    t._properties[o + a] = l, Array.isArray(l) ? t._properties[o + a] = new P(l, (function(t) {
                                        const n = a + "." + t.path,
                                            r = t.newValue,
                                            o = document.querySelector(e);
                                        if (o) {
                                            const e = n.split(".");
                                            let t = o;
                                            for (let n = 0; n < e.length; n++) t = t[e[n]];
                                            t = r
                                        }
                                    })) : (Object.defineProperty(n, a, { configurable: !1, enumerable: !0, get: () => t._properties[o + a], set(e) { t._properties[o + a] = e } }), l && "DataAdapter" === l.constructor.name || l && "object" == typeof l && Smart.DataAdapter && l instanceof Smart.DataAdapter || "object" == typeof l && l && Object.keys(l).length > 0 && r(l, o + a + "."))
                                }
                            };
                            r(n, ""), Object.defineProperty(t, "properties", { configurable: !1, enumerable: !0, get: () => n });
                            const o = document.querySelector(e);
                            if (o && o.isReady)
                                for (let e in n) o[e] = n[e];
                            else if (o) { o.props = {}; for (let e in n) o.props[e] = n[e] }
                        }(e, u[e]), u[e]) : void 0;
                        if (t) {
                            if (T.tagNames[e] = t, T.lazyRegister) { T.toRegister || (T.toRegister = []); const e = a.toCamelCase(r).replace(/[a-z]+/, ""); return window[n][e] = t, void T.toRegister.push({ tagName: r, element: t }) }
                            T.register(r, t)
                        }
                    }
                }, window.addEventListener("load", (function() {
                    const e = window[n].Elements.tagNames;
                    let t = [];
                    for (let r in e) {
                        const o = e[r];
                        let i = document.querySelectorAll("[" + r + "]");
                        for (let e = 0; e < i.length; e++) {
                            const t = i[e];
                            t instanceof HTMLDivElement && (t.__proto__ = o.prototype, t.created(), t.connectedCallback()), t.classList.add("smart-element-ready")
                        }
                        let s = o.name;
                        "Item" === s && (s = "ListItem"), i = document.querySelectorAll('[is="' + n.toLocaleLowerCase() + s + '"]');
                        for (let e = 0; e < i.length; e++) t.push(i[e])
                    }
                    if (t.length > 0) {
                        const e = e => {
                            let t = [],
                                n = e.parentNode;
                            for (; n && 9 !== n.nodeType;) n instanceof HTMLElement == 1 && t.push(n), n = n.parentNode;
                            return t
                        };
                        t.sort((function(t, n) {
                            let r = e(t).length,
                                o = e(n).length;
                            return r < o ? 1 : r > o ? -1 : 0
                        }));
                        for (let e = 0; e < t.length; e++) {
                            const n = t[e],
                                r = n.getAttribute("is");
                            let o;
                            o = "smartItem" === r ? new window.smartListItem(n) : new window[r](n), o.removeAttribute("is")
                        }
                    }
                }));
                const L = function() {
                    if ("complete" === document.readyState && "manual" !== window[n].RenderMode) {
                        x.sort((function(e, t) {
                            let n = e.element.parents.length,
                                r = t.element.parents.length;
                            return n < r ? -1 : n > r ? 1 : 0
                        }));
                        for (let e = 0; e < x.length; e++) window[n].RenderMode = "", x[e].element.isLoading = !1, x[e].callback(), window[n].RenderMode = "";
                        x = [], document.removeEventListener("readystatechange", L)
                    }
                };
                Object.assign(window[n], {
                    Elements: T,
                    Modules: [],
                    BaseElement: class extends _ {
                        static get observedAttributes() {
                            let e = this,
                                t = ["external-style"];
                            for (let n in e.prototype.extendedProperties) {
                                const r = e.prototype.extendedProperties[n];
                                t.push(r.attributeName)
                            }
                            return t
                        }
                        static get styleUrls() { return [] }
                        static get styles() { return "" }
                        get styleUrl() { return this._styleUrl }
                        set styleUrl(e) { this._styleUrl = e }
                        get isInShadowDOM() {
                            const e = this,
                                t = e.getRootNode();
                            return !e.hasAttribute("smart-blazor") && t !== document && t !== e
                        }
                        getShadowRootOrBody() { const e = this; return e.isInShadowDOM && e.getRootNode().host ? e.getRootNode().host.shadowRoot : document.body }
                        get enableShadowDOM() { return window[n].EnableShadowDOM }
                        importStyle(e, t) { this._importStyle(e, t) }
                        _importStyle(e, t) {
                            const n = this;
                            if (!n.shadowRoot || !e) return;
                            const r = e => { const r = n.shadowRoot.children; for (let n = 0; n < r.length; n++) { const o = r[n]; if (o instanceof HTMLLinkElement && o.href === e) return t && t(), null } const o = document.createElement("link"); return o.rel = "stylesheet", o.type = "text/css", o.href = e, o.onload = t, o },
                                o = (() => {
                                    const e = n.shadowRoot.children;
                                    let t = null;
                                    for (let n = 0; n < e.length; n++) {
                                        const r = e[n];
                                        r instanceof HTMLLinkElement && (t = r)
                                    }
                                    return t
                                })(),
                                i = (e, t) => { t.parentNode.insertBefore(e, t.nextSibling) };
                            if (Array.isArray(e)) {
                                const t = document.createDocumentFragment();
                                for (let n = 0; n < e.length; n++) {
                                    const o = r(e[n]);
                                    o && t.appendChild(o)
                                }
                                o ? i(t, o) : n.shadowRoot.insertBefore(t, n.shadowRoot.firstChild)
                            } else {
                                const t = r(e);
                                if (!t) return;
                                o ? i(t, o) : n.shadowRoot.insertBefore(t, n.shadowRoot.firstChild)
                            }
                        }
                        attributeChanged(e, t, n) { "style-url" === e && (this.styleUrl = n) }
                        attributeChangedCallback(e, t, n) { this.isReady && super.attributeChangedCallback(e, t, n) }
                        constructor(e, t) {
                            super();
                            const n = this;
                            if (e) {
                                t && (n._initProperties = t);
                                const r = e => {
                                    if ("string" == typeof e ? document.querySelector(e) : e) {
                                        const r = "string" == typeof e ? document.querySelector(e) : e;
                                        if (r instanceof HTMLDivElement) { const o = document.createElement(n.tagName); for (let e of r.attributes) o.setAttribute(e.name, r.getAttribute(e.name)); for (; r.childNodes.length;) o.appendChild(r.firstChild); return "string" == typeof e && (o.id = e.substring(1)), o._initProperties = t, r.parentNode && r.parentNode.replaceChild(o, r), o }
                                        if (t) {
                                            const e = r.context;
                                            if (r._initProperties = t, r.isReady) {
                                                r.context = r;
                                                const n = {},
                                                    o = {};
                                                for (let e in t) n[e] = r[e], o[e] = t[e];
                                                Object.getOwnPropertyNames(t).length > 0 && (r.initProperties(), r.propertyChangedHandler(t, n, o)), r.context = e
                                            }
                                        }
                                        return r
                                    }
                                };
                                if ("string" == typeof e) {
                                    const t = document.querySelectorAll(e),
                                        n = [];
                                    if (t.length > 1) {
                                        for (let e = 0; e < t.length; e++) {
                                            const o = r(t[e]);
                                            n.push(o)
                                        }
                                        return n
                                    }
                                } else if (e && e.length > 0) {
                                    const t = e;
                                    if (t.length > 1) {
                                        for (let e = 0; e < t.length; e++) {
                                            const n = r(t[e]);
                                            C.push(n)
                                        }
                                        return C
                                    }
                                }
                                return r(e)
                            }
                            n._styleUrl = "", n.isUtilityElement || n.created()
                        }
                        _getRootShadowParent() {
                            let e = this.shadowParent;
                            for (; e;) {
                                if (!e.shadowParent) return e;
                                e = e.shadowParent
                            }
                            return e || this.shadowParent
                        }
                        _getStyleUrl(e) { let t = y.Core.getScriptLocation() + window[n].StyleBaseUrl + e; return this.shadowParent && (t = t.replace("scoped/", "")), t }
                        _getStyleUrls() {
                            const e = this;
                            e.nodeName.startsWith(n);
                            const t = e.getStaticMember("styleUrls", "array"),
                                r = [];
                            for (let n = 0; n < t.length; n++) {
                                const o = t[n],
                                    i = e._getStyleUrl(o);
                                r.push(i)
                            }
                            return r
                        }
                        _setupShadowRoot() {
                            const e = this;
                            e.classList.add("smart-element-init");
                            const t = t => { t.$.root && (t.$.root.classList.add(n.toLowerCase() + "-element"), t.$.root.classList.add(e.nodeName.toLowerCase())), t.setup(), t.classList.remove("smart-element-init") };
                            if (document.adoptedStyleSheets)
                                if (window[n].AdoptedStyleSheets) window[n].AdoptedStyleSheetsLoaded ? (e.shadowRoot.adoptedStyleSheets = window[n].AdoptedStyleSheets, t(e)) : (e.shadowRoot.adoptedStyleSheets = window[n].AdoptedStyleSheets, window[n].AdoptedStyleSheetsLoadedQueue || (window[n].AdoptedStyleSheetsLoadedQueue = []), window[n].AdoptedStyleSheetsLoadedQueue.push(e));
                                else {
                                    const r = new CSSStyleSheet;
                                    let o = y.Core.getScriptLocation() + "/styles/smart.default.css";
                                    r.replace('@import url("' + o + '")').then((() => {
                                        if (t(e), window[n].AdoptedStyleSheetsLoaded = !0, window[n].AdoptedStyleSheetsLoadedQueue) {
                                            const e = window[n].AdoptedStyleSheetsLoadedQueue;
                                            for (let n = 0; n < e.length; n++) {
                                                const r = e[n];
                                                t(r)
                                            }
                                            delete window[n].AdoptedStyleSheetsLoadedQueue
                                        }
                                    })).catch((e => { console.error("Failed to load:", e) })), window[n].AdoptedStyleSheets = [r], document.adoptedStyleSheets = [r], e.shadowRoot.adoptedStyleSheets = window[n].AdoptedStyleSheets
                                }
                        }
                        connect() {
                            const e = this;
                            window[n].EnableShadowDOM && !e.shadowRoot && !0 !== e.isInShadowDOM && (e.attachShadow({ mode: "open" }), e.shadowRoot && e.$.root && (e.shadowRoot.appendChild(e.$.root), e.$.root.classList.add(e.nodeName.toLowerCase()))), e.shadowRoot || e.shadowParent ? e.shadowRoot ? e._setupShadowRoot() : (e.shadowParent && window[n].EnableShadowDOM, e.setup()) : e.setup()
                        }
                        connectedCallback() {
                            const e = this;
                            if (e.isLoading || e.isUtilityElement) return;
                            e.classList.add("smart-element-init");
                            const t = function() { e.classList.remove("smart-element-init") };
                            if ("complete" === document.readyState && (void 0 === window[n].isAngular && (window[n].isAngular = null !== document.body.querySelector("[ng-version]")), window[n].isAngular))
                                for (let t = 0; t < e.parents.length && !e.parents[t].nodeName.toLowerCase().startsWith(n.toLowerCase() + "-"); t++)
                                    if (e.parents[t].hasAttribute("ng-version") && !e.classList.contains("smart-angular")) { window[n].RenderMode = "manual"; break }
                            if ("complete" === document.readyState && "manual" !== window[n].RenderMode) {
                                const n = e.parents;
                                n.length && "HTML" === n[n.length - 1].nodeName || e.getRootNode().host ? (e.checkIsInDomTimer && clearInterval(e.checkIsInDomTimer), t(), e.connect()) : (e.checkIsInDomTimer && clearInterval(e.checkIsInDomTimer), n.length > 0 && (e.checkIsInDomTimer = setInterval((() => {
                                    const n = e.parents;
                                    0 === n.length && clearInterval(e.checkIsInDomTimer), n.length > 0 && "HTML" === n[n.length - 1].nodeName && (clearInterval(e.checkIsInDomTimer), t(), e.connect())
                                }), 100)))
                            } else e.isLoading = !0, x.push({ element: this, callback: function() { this.isReady || (t(), this.connect()) }.bind(e) })
                        }
                        disconnectedCallback() {
                            const e = this;
                            e.isAttached ? (e.shadowParent = null, e.detached()) : e._resetShadowParent()
                        }
                        adoptedCallback() { this.setup() }
                        appendTemplate(e) {
                            const t = this;
                            t.shadowRoot ? t.shadowRoot.appendChild(e) : t.appendChild(e)
                        }
                        _resetShadowParent() {
                            const e = this;
                            if (!window[n].EnableShadowDOM || null === e.shadowParent) return;
                            const t = [];
                            let r = e.parentNode;
                            for (; r && 9 !== r.nodeType;) {
                                if (r instanceof HTMLElement == 1) t.push(r);
                                else if (11 === r.nodeType && r.host) { r = r.host; continue }
                                r = r.parentNode
                            }
                            for (let n = 0; n < t.length; n++)
                                if (t[n] === e.shadowParent) return;
                            t.length > 0 && "HTML" === t[t.length - 1].nodeName && (e.shadowParent = null)
                        }
                    },
                    Utilities: y,
                    Import: function(e, t) {
                        let n = 0;
                        const r = function(e, t) {
                            return new Promise((n => {
                                const r = document.createElement("script");
                                r.src = e, r.onload = n;
                                for (let e = 0; e < document.head.children.length; e++) { const r = document.head.children[e]; if (r.src && r.src.toString().indexOf(t) >= 0) return void n() }
                                document.head.appendChild(r)
                            }))
                        };
                        return new Promise((o => {
                            const i = y.Core.getScriptLocation(),
                                s = function(t) {
                                    if (!e[t]) return;
                                    const a = i + "/" + e[t];
                                    r(a, e[t]).then((function() { n++, n === e.length && o(), s(t + 1) }))
                                };
                            if (t)
                                for (let t = 0; t < e.length; t++) {
                                    const s = i + "/" + e[t];
                                    r(s, e[t]).then((function() { n++, n === e.length && o() }))
                                } else s(0)
                        }))
                    },
                    ObservableArray: P,
                    Observable: class {
                        constructor(e, t) { const n = this; var r; return this.name = "observable", e && Object.assign(n, e), r = e, Object.getOwnPropertyNames(Object.getPrototypeOf(r)).forEach((e => "constructor" === e || !!e.startsWith("_") || void(n[e] = r[e]))), new Proxy(n, { deleteProperty: function(e, t) { return delete e[t], !0 }, get: function(e, t) { return e[t] }, set: function(e, r, o) { const i = e[r]; return i === o || (e[r] = o, !("notifyFn" !== r && !r.startsWith("_") && "canNotify" !== r && (!t || -1 !== t.indexOf(r)) && n.canNotify && (n._notify({ target: e, propertyName: r, oldValue: i, newValue: o }), 0))) } }) }
                        get canNotify() { const e = this; return void 0 === e._canNotify && (e._canNotify = !0), e._canNotify }
                        set canNotify(e) { this._canNotify = e }
                        _notify(e) {
                            const t = this;
                            if (t.canNotify && t.notifyFn)
                                for (let n = 0; n < t.notifyFn.length; n++) t.notifyFn[n](e)
                        }
                        notify(e) {
                            const t = this;
                            e && (t.notifyFn || (t.notifyFn = []), t.notifyFn.push(e))
                        }
                    },
                    Component: class {
                        constructor(e, t) { const n = this.name; let r = null; return e ? r = new window[n](e, t) : (r = new window[n], r._initProperties = t), this._element = r, r }
                        get name() { return "Component" }
                        get element() { return this._element }
                    },
                    Theme: D.Theme || "",
                    EnableShadowDOM: D.ShadowDom || !1,
                    BaseUrl: "./",
                    StyleBaseUrl: "/styles/default/",
                    Version: e,
                    Templates: t,
                    RenderMode: D.RenderMode || "auto",
                    Render: function() { const e = () => { window[n].RenderMode = "", L() }; "complete" === document.readyState ? e() : (window.removeEventListener("load", e), window.addEventListener("load", e)) },
                    Data: u,
                    Mode: D.Mode || "production",
                    License: "Evaluation"
                });
                let O = window[n].Theme;
                "manual" !== window[n].RenderMode && document.addEventListener("readystatechange", L), Object.defineProperty(window[n], "Theme", {
                    configurable: !1,
                    enumerable: !0,
                    get: () => O,
                    set(e) {
                        const t = O;
                        O = e, w.fireEvent("theme-changed", { oldValue: t, newValue: e }, { bubbles: !0, cancelable: !0 })
                    }
                }), window[n]("smart-base-element", window[n].BaseElement), window[n]("smart-content-element", class extends window[n].BaseElement {
                    static get properties() { return { content: { type: "any", reflectToAttribute: !1 }, innerHTML: { type: "string", reflectToAttribute: !1 } } }
                    template() { return "<div inner-h-t-m-l='[[innerHTML]]'></div>" }
                    ready() { super.ready(), this.applyContent() }
                    refresh() {}
                    clearContent() { const e = this; for (; e.$.content.firstChild;) e.$.content.removeChild(e.$.content.firstChild) }
                    applyContent() {
                        const e = this;
                        if (void 0 === e.content) return void(e.content = e.$.content);
                        if ("" === e.content || null === e.content) return void e.clearContent();
                        if (e.content instanceof HTMLElement) return e.clearContent(), void e.$.content.appendChild(e.content);
                        const t = document.createDocumentFragment();
                        let n = document.createElement("div");
                        t.appendChild(n), e.content instanceof HTMLElement ? n.appendChild(e.content) : n.innerHTML = e.content;
                        let r = Array.from(n.childNodes);
                        n.parentNode.removeChild(n);
                        for (let e = 0; e < r.length; e++) t.appendChild(r[e]);
                        e.clearContent(), e.$.content.appendChild(t)
                    }
                    propertyChangedHandler(e, t, n) {
                        super.propertyChangedHandler(e, t, n);
                        const r = this;
                        t !== n && ("innerHTML" === e && (r.content = n, r.applyContent(), r.innerHTML = r.content = y.Core.html(r.$.content)), "content" === e && r.applyContent())
                    }
                }), window[n]("smart-scroll-viewer", class extends window[n].ContentElement {
                    static get properties() { return { horizontalScrollBarVisibility: { type: "string", value: "auto", allowedValues: ["auto", "disabled", "hidden", "visible"] }, touchScrollRatio: { type: "any", value: null }, touchVelocityCoefficient: { type: "number", value: 50 }, verticalScrollBarVisibility: { type: "string", value: "auto", allowedValues: ["auto", "disabled", "hidden", "visible"] } } }
                    static get listeners() { return { touchmove: "_touchmoveHandler", touchstart: "_touchstartHandler", wheel: "_mouseWheelHandler", "document.up": "_upHandler" } }
                    static get styleUrls() { return ["smart.scrollviewer.css"] }
                    template() { return '<div id="container" class="smart-container" role="presentation">\n                        <div id="scrollViewerContainer" class="smart-scroll-viewer-container" role="presentation">\n                            <div id="scrollViewerContentContainer" inner-h-t-m-l=\'[[innerHTML]]\' class="smart-scroll-viewer-content-container" role="presentation">\n                                <content></content>\n                            </div>\n                        </div>\n                        <smart-scroll-bar id="verticalScrollBar" theme="[[theme]]"  animation="[[animation]]" disabled="[[disabled]]" right-to-left="[[rightToLeft]]" orientation="vertical"></smart-scroll-bar>\n                        <smart-scroll-bar id="horizontalScrollBar" theme="[[theme]]" disabled="[[disabled]]" right-to-left="[[rightToLeft]]"></smart-scroll-bar>\n                    </div>' }
                    appendChild(e) {
                        const t = this;
                        if (e) {
                            if (!t.isCompleted || e.classList && e.classList.contains("smart-resize-trigger-container")) { const e = Array.prototype.slice.call(arguments, 2); return HTMLElement.prototype.appendChild.apply(t, e.concat(Array.prototype.slice.call(arguments))) }
                            t.$.scrollViewerContentContainer.appendChild(e)
                        }
                    }
                    removeChild(e) {
                        const t = this;
                        if (e) {
                            if (!t.isCompleted || e.classList && e.classList.contains("smart-resize-trigger-container")) { const e = Array.prototype.slice.call(arguments, 2); return HTMLElement.prototype.removeChild.apply(t, e.concat(Array.prototype.slice.call(arguments))) }
                            t.$.scrollViewerContentContainer.removeChild(e)
                        }
                    }
                    removeAll() {
                        const e = this;
                        e.isCompleted && (e.$.scrollViewerContentContainer.innerHTML = "")
                    }
                    _horizontalScrollbarHandler(e) {
                        const t = this;
                        t.$.scrollViewerContentContainer.style.left = (t.rightToLeft ? 1 : -1) * t.scrollLeft + "px", e.stopPropagation && e.stopPropagation(), t.onHorizontalChange && t.onHorizontalChange(e)
                    }
                    _verticalScrollbarHandler(e) {
                        const t = this;
                        t.$.scrollViewerContentContainer.style.top = -t.scrollTop + "px", e.stopPropagation && e.stopPropagation(), t.onVerticalChange && t.onVerticalChange(e)
                    }
                    _touchmoveHandler(e) {
                        const t = this;
                        if (t._touchmoveInside && e.cancelable) return e.preventDefault(), void e.stopPropagation();
                        const n = t.scrollHeight > 0,
                            r = t.scrollWidth > 0,
                            o = t._touchCoords;
                        if (!n && !r || !o) return;
                        const i = e.touches[0];
                        let s, a, l, d;
                        t._touchCoords = [i.pageX, i.pageY], n ? (s = t.scrollTop, a = t.scrollHeight, l = i.pageY, d = o[1]) : (s = t.scrollLeft, a = t.scrollWidth, l = i.pageX, d = o[0]);
                        const c = parseFloat(l.toFixed(5)),
                            u = parseFloat(d.toFixed(5));
                        0 === s && c >= u || s === a && c <= u || (l !== d && (t._touchmoveInside = !0), e.cancelable && (e.preventDefault(), e.stopPropagation()))
                    }
                    _touchstartHandler(e) {
                        const t = e.touches[0];
                        this._touchCoords = [t.pageX, t.pageY]
                    }
                    _mouseWheelHandler(e) {
                        const t = this;
                        if (!t.disabled && (t.computedHorizontalScrollBarVisibility || t.computedVerticalScrollBarVisibility)) {
                            if (e.shiftKey && t.computedHorizontalScrollBarVisibility) { const n = t.scrollLeft; if (0 === n && e.deltaX < 0 || n === t.scrollHeight && e.deltaX > 0) return; return e.stopPropagation(), e.preventDefault(), void(t.scrollWidth > 0 && t.scrollTo(void 0, t.scrollLeft + t._getScrollCoefficient(e, t.offsetWidth))) }
                            if (t.computedVerticalScrollBarVisibility) {
                                const n = t.scrollTop;
                                if (0 === n && e.deltaY < 0 || n === t.scrollHeight && e.deltaY > 0) return;
                                e.stopPropagation(), e.preventDefault(), t.scrollHeight > 0 && t.scrollTo(t.scrollTop + t._getScrollCoefficient(e, t.offsetHeight))
                            }
                        }
                    }
                    _overriddenHandler() {}
                    _upHandler() { delete this._touchCoords, delete this._touchmoveInside }
                    _getScrollCoefficient(e, t) {
                        const n = e.deltaMode,
                            r = Math.abs(e.deltaY);
                        let o;
                        return 0 === n ? o = r < 100 / 3 ? r : t : 1 === n ? o = r < 1 ? r * (100 / 3) : t : 2 === n && (o = t), e.deltaY < 0 ? -o : o
                    }
                    applyContent() { super.applyContent(), this.refresh() }
                    get computedHorizontalScrollBarVisibility() { const e = this; return e._scrollView && e._scrollView.hScrollBar ? !e._scrollView.hScrollBar.$.hasClass("smart-hidden") : null }
                    get computedVerticalScrollBarVisibility() { const e = this; return e._scrollView && e._scrollView.vScrollBar ? !e._scrollView.vScrollBar.$.hasClass("smart-hidden") : null }
                    scrollTo(e, t) {
                        const n = this;
                        n._scrollView && (void 0 !== e && n._scrollView.scrollTo(e), void 0 !== t && n._scrollView.scrollTo(t, !1))
                    }
                    refreshScrollBarsVisibility() {
                        const e = this;
                        e._scrollView && (e._scrollView.hScrollBar.disabled = e.disabled, e._scrollView.vScrollBar.disabled = e.disabled, "disabled" === e.horizontalScrollBarVisibility && (e._scrollView.hScrollBar.disabled = !0), "disabled" === e.verticalScrollBarVisibility && (e._scrollView.vScrollBar.disabled = !0), e.scrollWidth > 0 ? e._scrollView.hScrollBar.$.removeClass("smart-hidden") : "visible" !== e.horizontalScrollBarVisibility && e._scrollView.hScrollBar.$.addClass("smart-hidden"), e.scrollHeight > 0 ? e._scrollView.vScrollBar.$.removeClass("smart-hidden") : "visible" !== e.verticalScrollBarVisibility && e._scrollView.vScrollBar.$.addClass("smart-hidden"), "hidden" === e.horizontalScrollBarVisibility && e._scrollView.hScrollBar.$.addClass("smart-hidden"), "hidden" === e.verticalScrollBarVisibility && e._scrollView.vScrollBar.$.addClass("smart-hidden"), "visible" === e.horizontalScrollBarVisibility && e._scrollView.hScrollBar.$.removeClass("smart-hidden"), "visible" === e.verticalScrollBarVisibility && (e._scrollView.vScrollBar.$.removeClass("smart-hidden"), e.disabled || (e._scrollView.vScrollBar.disabled = e.scrollHeight <= 0)), e.computedHorizontalScrollBarVisibility && e.computedVerticalScrollBarVisibility ? (e._scrollView.hScrollBar.$.addClass("bottom-corner"), e._scrollView.vScrollBar.$.addClass("bottom-corner")) : (e._scrollView.hScrollBar.$.removeClass("bottom-corner"), e._scrollView.vScrollBar.$.removeClass("bottom-corner")))
                    }
                    ready() {
                        super.ready();
                        const e = this;
                        e.$.verticalScrollBar.onChange = t => { t.detail = t, e._verticalScrollbarHandler(t) }, e.$.horizontalScrollBar.onChange = t => { t.detail = t, e._horizontalScrollbarHandler(t) }, e.$.verticalScrollBar.setAttribute("aria-controls", e.id), e.$.horizontalScrollBar.setAttribute("aria-controls", e.id), e._customScrollView || (e._scrollView = new Smart.Utilities.Scroll(e, e.$.horizontalScrollBar, e.$.verticalScrollBar)), e.refresh()
                    }
                    refresh() {
                        const e = this;

                        function t() {
                            const t = e.$.scrollViewerContainer.classList.contains("vscroll");
                            e.$.scrollViewerContainer.classList.remove("vscroll");
                            const n = e.$.scrollViewerContentContainer.offsetWidth - e.$.scrollViewerContainer.offsetWidth;
                            return n > 0 && "hidden" !== e.horizontalScrollBarVisibility || "visible" === e.horizontalScrollBarVisibility ? e.$.scrollViewerContainer.classList.add("hscroll") : e.$.scrollViewerContainer.classList.remove("hscroll"), t && e.$.scrollViewerContainer.classList.add("vscroll"), n
                        }

                        function n() {
                            let t;
                            const n = e.$.scrollViewerContainer.classList.contains("hscroll");
                            if (e.$.scrollViewerContainer.classList.remove("hscroll"), Smart.Utilities.Core.Browser.Safari) {
                                const n = e.$.scrollViewerContentContainer.getBoundingClientRect().height,
                                    r = e.$.scrollViewerContainer.getBoundingClientRect().height;
                                t = n && r ? parseInt(n) - parseInt(r) : e.$.scrollViewerContentContainer.offsetHeight - e.$.scrollViewerContainer.offsetHeight
                            } else t = e.$.scrollViewerContentContainer.offsetHeight - e.$.scrollViewerContainer.offsetHeight;
                            return e.virtualScrollHeight && (t = e.virtualScrollHeight), t > 0 && "hidden" !== e.verticalScrollBarVisibility || "visible" === e.verticalScrollBarVisibility ? e.$.scrollViewerContainer.classList.add("vscroll") : e.$.scrollViewerContainer.classList.remove("vscroll"), n && e.$.scrollViewerContainer.classList.add("hscroll"), t
                        }
                        if (!e.$.scrollViewerContentContainer) return;
                        let r = e.scrollWidth,
                            o = e.scrollHeight;
                        e.scrollWidth = t(), e.scrollHeight = n(), e.scrollHeight && o === e.scrollHeight || (e.scrollWidth = t()), e.scrollWidth && r === e.scrollWidth || (e.scrollHeight = n()), e.computedVerticalScrollBarVisibility && (e.scrollHeight += e._scrollView.hScrollBar.offsetHeight), e.computedHorizontalScrollBarVisibility && (e.scrollWidth += e._scrollView.vScrollBar.offsetWidth), 0 === e.scrollHeight && e.scrollWidth > 0 && e.$.container.offsetHeight - e.$.content.offsetHeight < 5 && (e.$.container.style.paddingBottom = e._scrollView.hScrollBar.offsetHeight + "px")
                    }
                    attached() {
                        const e = this;
                        super.attached(), e._scrollView || e._customScrollView || (e._scrollView = new Smart.Utilities.Scroll(e, e.$.horizontalScrollBar, e.$.verticalScrollBar))
                    }
                    detached() {
                        const e = this;
                        super.detached(), e._scrollView && (e._scrollView.unlisten(), delete e._scrollView)
                    }
                    get scrollWidth() { const e = this; return e._scrollView && e._scrollView.hScrollBar ? 1 === e._scrollView.hScrollBar.max && "visible" === e.horizontalScrollBarVisibility ? 0 : e._scrollView.hScrollBar.max : -1 }
                    set scrollWidth(e) {
                        const t = this;
                        e < 0 && (e = 0), t._scrollView && t._scrollView.hScrollBar && (0 === e && "visible" === t.horizontalScrollBarVisibility ? t._scrollView.hScrollBar.max = 0 : t._scrollView.hScrollBar.max = e, t.refreshScrollBarsVisibility())
                    }
                    get scrollHeight() { const e = this; return e._scrollView && e._scrollView.vScrollBar ? 1 === e._scrollView.vScrollBar.max && "visible" === e.verticalScrollBarVisibility ? 0 : e._scrollView.vScrollBar.max : 0 }
                    set scrollHeight(e) {
                        const t = this;
                        e < 0 && (e = 0), t._scrollView && t._scrollView.vScrollBar && (0 === e && "visible" === t.verticalScrollBarVisibility ? t._scrollView.vScrollBar.max = 1 : t._scrollView.vScrollBar.max = e, t.refreshScrollBarsVisibility())
                    }
                    get scrollLeft() { const e = this; return e._scrollView && e._scrollView.hScrollBar ? e._scrollView.hScrollBar.value : 0 }
                    set scrollLeft(e) {
                        const t = this;
                        e < 0 && (e = 0), t._scrollView && t._scrollView.hScrollBar && (t._scrollView.hScrollBar.value = e)
                    }
                    get scrollTop() { const e = this; return e._scrollView && e._scrollView.vScrollBar ? e._scrollView.vScrollBar.value : 0 }
                    set scrollTop(e) {
                        const t = this;
                        e < 0 && (e = 0), t._scrollView && t._scrollView.vScrollBar && (t._scrollView.vScrollBar.value = e)
                    }
                    propertyChangedHandler(e, t, n) {
                        const r = this;
                        super.propertyChangedHandler(e, t, n), "animation" !== e && "theme" !== e && r.refresh()
                    }
                }), window[n].Utilities.Assign("PositionDetection", class {
                    constructor(e, t, n, r) {
                        const o = this;
                        if (t) {
                            const n = "dropDown" + Math.floor(65536 * (1 + Math.random())).toString(16).substring(1);
                            t.id = n, e.setAttribute("aria-owns", n)
                        }
                        o.context = e, o.dropDown = t, o.defaultParent = n, o.closeMethod = r
                    }
                    handleAutoPositioning() {
                        const e = this,
                            t = e.context;
                        if ("auto" !== t.dropDownPosition || t.disabled || t.isHidden) return;
                        const n = window.requestAnimationFrame;
                        let r, o = Date.now();
                        return r = n((function i() { t.isHidden || document.hidden || (r = n(i), "auto" === t.dropDownPosition && !t.disabled && (t.isInShadowDOM ? document.body.contains(t.shadowParent) : document.body.contains(t)) || cancelAnimationFrame(r), t.isHidden && cancelAnimationFrame(r), Date.now() - o >= 200 && (e.scrollHandler(), o = Date.now())) }))
                    }
                    checkBrowserBounds(e) {
                        const t = this.context;
                        if ("auto" === t.dropDownPosition && !t.disabled) switch (e) {
                            case "vertically":
                                this.checkBrowserBoundsVertically();
                                break;
                            case "horizontally":
                                this.checkBrowserBoundsHorizontally();
                                break;
                            default:
                                this.checkBrowserBoundsVertically(), this.checkBrowserBoundsHorizontally()
                        }
                    }
                    checkBrowserBoundsHorizontally() {
                        const e = this.context,
                            t = this.dropDown;
                        let n, r = 0;
                        a.isMobile || window.innerWidth === document.documentElement.clientWidth || (r = window.innerWidth - document.documentElement.clientWidth), null !== e._dropDownParent ? n = !0 : t.style.left = "";
                        const o = window.innerWidth - r;
                        let i = e.getBoundingClientRect().left;
                        if (i < 0 && (t.style.left = (n ? 0 : Math.abs(i)) + "px", i = parseFloat(t.style.left)), i + t.offsetWidth > o) {
                            let e = i - Math.abs(o - i - t.offsetWidth);
                            n && (e += window.pageXOffset), t.style.left = (n ? e : e - i) + "px", window.innerWidth === document.documentElement.clientWidth && (t.style.left = parseFloat(t.style.left) + r + "px"), n && window.innerHeight === document.documentElement.clientHeight && this.positionDropDown(!0)
                        }
                    }
                    checkBrowserBoundsVertically(e) {
                        const t = this.context,
                            n = this.dropDown,
                            r = t._dropDownListPosition;
                        e || (e = t.getBoundingClientRect()), 0 !== e.height && (document.documentElement.clientHeight - Math.abs(e.top + e.height + n.offsetHeight) >= 0 ? t._dropDownListPosition = "bottom" : e.top - n.offsetHeight >= 0 ? t._dropDownListPosition = "top" : t._dropDownListPosition = "overlay-center", this.updatePositionAttribute(r, t._dropDownListPosition))
                    }
                    scrollHandler() {
                        const e = this.context;
                        if (!e.parentElement) return;
                        const t = e.getBoundingClientRect();
                        if (t.top === e._positionTop) return;
                        const n = e._dropDownListPosition;
                        this.checkBrowserBoundsVertically(t), e._dropDownListPosition !== n && this.positionDropDown(), e._positionTop = t.top
                    }
                    getDropDownParent(e) {
                        const t = this.context,
                            n = this.dropDown;
                        let r = t.dropDownAppendTo;
                        t._positionedParent = null, null === r ? t._dropDownParent = null : "body" === r || r === document.body ? t.getRootNode().host ? t._dropDownParent = t.getRootNode().host.shadowRoot : t._dropDownParent = document.body : r instanceof HTMLElement ? t._dropDownParent = r : "string" == typeof r ? (r = document.getElementById(r), r instanceof HTMLElement ? t._dropDownParent = r : (t.dropDownAppendTo = null, t._dropDownParent = null)) : (t.dropDownAppendTo = null, t._dropDownParent = null);
                        let o = t._dropDownParent;
                        if (null !== o) {
                            for (; o && o instanceof HTMLElement && "static" === window.getComputedStyle(o).position && o !== t.getShadowRootOrBody();) o = o.parentElement;
                            o === document.body ? t._positionedParent = null : t._positionedParent = o, n && (n.setAttribute("animation", t.animation), "" !== t.theme && n.$.addClass(t.theme), e && (t._dropDownParent.appendChild(n), n.$.addClass("smart-drop-down-repositioned")), -1 === t.detachedChildren.indexOf(n) && t.detachedChildren.push(n))
                        }
                    }
                    dropDownAppendToChangedHandler() {
                        const e = this.context,
                            t = this.dropDown,
                            n = e._dropDownParent;
                        this.getDropDownParent(), e._dropDownParent !== n && (e[this.closeMethod](), ["left", "top", "font-size", "font-family", "font-style", "font-weight"].forEach((e => t.style[e] = null)), null === e._dropDownParent ? (this.defaultParent.appendChild(t), t.$.removeClass("smart-drop-down-repositioned")) : (e._dropDownParent.appendChild(t), t.$.addClass("smart-drop-down-repositioned")))
                    }
                    dropDownPositionChangedHandler() {
                        const e = this;
                        e.dropDown.style.transition = "none", e.context[e.closeMethod](), e.setDropDownPosition(), e.handleAutoPositioning()
                    }
                    dropDownAttached(e) {
                        const t = this.context;
                        null !== t._dropDownParent && (t._dropDownParent.appendChild(this.dropDown), this.handleAutoPositioning(), e && t[e]())
                    }
                    dropDownDetached() {
                        const e = this.context;
                        null !== e._dropDownParent && document.body.contains(this.dropDown) && document.body.contains(e._dropDownParent) && e._dropDownParent.removeChild(this.dropDown)
                    }
                    setDropDownPosition() {
                        const e = this.context,
                            t = e.dropDownPosition,
                            n = e._dropDownListPosition;
                        "auto" === t ? this.checkBrowserBounds() : e._dropDownListPosition = t, this.updatePositionAttribute(n, e._dropDownListPosition)
                    }
                    updatePositionAttribute(e, t) {
                        const n = this.context,
                            r = this.dropDown;
                        n.$.dropDownButton && !n.$.dropDownButton.hasAttribute(t) && (n.$.dropDownButton.removeAttribute(e), n.$.dropDownButton.setAttribute(t, "")), r.hasAttribute(t) || (r.style.transition = "none", r.removeAttribute(e), r.setAttribute(t, ""), requestAnimationFrame((function() { r.style.transition = null })))
                    }
                    positionDropDown(e) {
                        const t = this.context,
                            n = this.dropDown;
                        if (!t.opened || null === t._dropDownParent) return;
                        const r = t.getBoundingClientRect();
                        let o, i;
                        if (this.customPositionDropDown) {
                            const e = this.customPositionDropDown(r);
                            o = e.left, i = e.top
                        } else switch (o = r.left, i = r.top, t._dropDownListPosition) {
                            case "bottom":
                                i += t.$.container.offsetHeight - 1;
                                break;
                            case "center-bottom":
                                i += t.$.container.offsetHeight - 1, o += t.offsetWidth - n.offsetWidth / 2;
                                break;
                            case "center-top":
                                i -= n.offsetHeight - 1, o += t.offsetWidth - n.offsetWidth / 2;
                                break;
                            case "top":
                                i -= n.offsetHeight - 1;
                                break;
                            case "overlay-bottom":
                                break;
                            case "overlay-center":
                                i -= n.offsetHeight / 2 - t.offsetHeight / 2;
                                break;
                            case "overlay-top":
                                i -= n.offsetHeight - t.offsetHeight
                        }
                        const s = this.getDropDownOffset();
                        n.style.top = i + s.y + "px", e || (n.style.left = o + s.x + "px")
                    }
                    getDropDownOffset() {
                        const e = this.context._positionedParent;
                        let t, n;
                        if (e && "#document-fragment" !== e.nodeName) {
                            const r = e.getBoundingClientRect();
                            t = -r.left, n = -r.top
                        } else t = window.pageXOffset, n = window.pageYOffset;
                        return { x: t, y: n }
                    }
                    placeOverlay() {
                        const e = this.context;
                        if (!e.dropDownOverlay || e._overlay) return;
                        const t = document.createElement("div");
                        t.classList.add("smart-drop-down-overlay"), t.style.width = document.documentElement.scrollWidth + "px", t.style.height = document.documentElement.scrollHeight + "px", document.body.appendChild(t), e._overlay = t
                    }
                    removeOverlay(e) {
                        const t = this,
                            n = t.context;
                        n._overlay && (n.hasAnimation && e ? requestAnimationFrame((function e() { t.dropDown.getBoundingClientRect().height > 0 ? requestAnimationFrame(e) : (document.body.removeChild(n._overlay), delete n._overlay) })) : (document.body.removeChild(n._overlay), delete n._overlay))
                    }
                }), window.Smart.Color = class {
                    constructor(e) {
                        if (window.Smart._colors || (window.Smart._colors = []), window.Smart._colors[e]) { const t = window.Smart._colors[e]; return this.hex = t.hex, this.r = t.r, this.g = t.g, void(this.b = t.b) }
                        this.r = this.g = this.b = 0, this.hex = "";
                        const t = this.getStandardizedColor(e);
                        t && (this.setHex(t.substring(1)), window.Smart._colors[e] = { hex: this.hex, r: this.r, g: this.g, b: this.b })
                    }
                    getStandardizedColor(e) { const t = document.createElement("canvas").getContext("2d"); return t.fillStyle = e, t.fillStyle }
                    getInvertedColor() { return "" === this.hex ? "transparent" : 255 - (.299 * this.r + .587 * this.g + .114 * this.b) < 105 ? "Black" : "White" }
                    hexToRgb(e) {
                        let t = "00",
                            n = "00",
                            r = "00";
                        return 6 === (e = this.validateHex(e)).length ? (t = e.substring(0, 2), n = e.substring(2, 4), r = e.substring(4, 6)) : (e.length > 4 && (t = e.substring(4, e.length), e = e.substring(0, 4)), e.length > 2 && (n = e.substring(2, e.length), e = e.substring(0, 2)), e.length > 0 && (r = e.substring(0, e.length))), { r: this.hexToInt(t), g: this.hexToInt(n), b: this.hexToInt(r) }
                    }
                    validateHex(e) { return (e = (e = new String(e).toUpperCase()).replace(/[^A-F0-9]/g, "0")).length > 6 && (e = e.substring(0, 6)), e }
                    webSafeDec(e) { return e = Math.round(e / 51), e *= 51 }
                    hexToWebSafe(e) { let t, n, r; return 3 === e.length ? (t = e.substring(0, 1), n = e.substring(1, 1), r = e.substring(2, 1)) : (t = e.substring(0, 2), n = e.substring(2, 4), r = e.substring(4, 6)), this.intToHex(this.webSafeDec(this.hexToInt(t))) + this.intToHex(this.webSafeDec(this.hexToInt(n))) + this.intToHex(this.webSafeDec(this.hexToInt(r))) }
                    rgbToWebSafe(e) { return { r: this.webSafeDec(e.r), g: this.webSafeDec(e.g), b: this.webSafeDec(e.b) } }
                    rgbToHex(e) { return this.intToHex(e.r) + this.intToHex(e.g) + this.intToHex(e.b) }
                    intToHex(e) { let t = parseInt(e).toString(16); return 1 === t.length && (t = "0" + t), t.toUpperCase() }
                    hexToInt(e) { return parseInt(e, 16) }
                    setRgb(e, t, n) {
                        let r = function(e) { return e < 0 || e > 255 || isNaN(parseInt(e)) ? 0 : e };
                        this.r = r(e), this.g = r(t), this.b = r(n), this.hex = this.rgbToHex(this)
                    }
                    setHex(e) {
                        this.hex = e;
                        let t = this.hexToRgb(this.hex);
                        this.r = t.r, this.g = t.g, this.b = t.b
                    }
                }
            }();

            /***/
        }),

        /***/
        3661:
        /***/
            (() => {

            Smart("smart-menu-item", class extends Smart.BaseElement {
                static get properties() { return { checked: { value: !1, type: "boolean" }, label: { value: "", type: "any" }, level: { value: null, type: "number?" }, separator: { value: !1, type: "boolean" }, shortcut: { value: "", type: "string" }, value: { value: null, type: "any" } } }
                get enableShadowDOM() { return !1 }
                template() { return "" }
                ready() {
                    const e = this;
                    if (super.ready(), e.$.addClass("smart-unselectable"), e.setAttribute("role", "menuitem"), e.checked && e.setAttribute("aria-checked", !0), !1 === e.isDirty) return;
                    const t = e.closest("smart-menu, smart-tree");
                    t && t.isRendered && (cancelAnimationFrame(Smart.Menu.processTimer), Smart.Menu.processTimer = requestAnimationFrame((() => { t._lazyInitItems() })))
                }
                propertyChangedHandler(e, t, n) {
                    const o = this;
                    if (super.propertyChangedHandler(e, t, n), "smart-tree-item" === o.tagName.toLowerCase()) return;
                    const i = o.menu,
                        r = o.parentItem,
                        a = r || i;
                    if ("label" === e) return "" === n ? void(o.label = t) : (o.setAttribute("aria-label", n), void(i && i._setItemLabel(o, n)));
                    if (!i) return;
                    if ("separator" === e) return void i._refreshCheckableItems(a);
                    if ("disabled" !== e || !1 === n || !o.checked) return;
                    super.propertyChangedHandler(e, t, n), o.checked = !1;
                    const s = a.checkMode;
                    "radioButton" === s ? i._validateRadioButtonSelection(r, o.level, []) : "checkbox" !== s && i._refreshCheckableItems(a)
                }
            }), Smart("smart-menu-items-group", class extends Smart.BaseElement {
                static get properties() { return { checkable: { value: !1, type: "boolean" }, checked: { value: !1, type: "boolean" }, checkMode: { value: "checkbox", type: "string" }, dropDownHeight: { value: null, type: "number?" }, expanded: { value: !1, type: "boolean" }, label: { value: "", type: "any" }, level: { value: null, type: "number?" }, separator: { value: !1, type: "boolean" }, value: { value: null, type: "any" } } }
                get enableShadowDOM() { return !1 }
                template() { return "" }
                ready() {
                    const e = this;
                    if (super.ready(), e.$.addClass("smart-unselectable"), e.setAttribute("role", "menuitem"), e.setAttribute("aria-haspopup", !0), e.setAttribute("aria-expanded", e.expanded), e.checked && e.setAttribute("aria-checked", !0), !1 === e.isDirty) return;
                    const t = e.closest("smart-menu, smart-tree");
                    t && t.isRendered && (cancelAnimationFrame(Smart.Menu.processTimer), Smart.Menu.processTimer = requestAnimationFrame((() => { t._lazyInitItems() })))
                }
                propertyChangedHandler(e, t, n) {
                    const o = this;
                    if (super.propertyChangedHandler(e, t, n), "smart-tree-items-group" === o.tagName.toLowerCase()) return;
                    const i = o.menu,
                        r = o.parentItem,
                        a = r || i;
                    if ("label" === e) return "" === n ? void(o.label = t) : (o.setAttribute("aria-label", n), void(i && i._setItemLabel(o, n)));
                    if (i && -1 !== ["checkable", "checkMode", "disabled", "separator"].indexOf(e)) switch (e) {
                        case "checkable":
                            n ? o.itemContainer.setAttribute("checkable", "") : o.itemContainer.removeAttribute("checkable"), i._isContainerOpened(o.container.level, o.container) && "tree" !== i.mode && !i._minimized && i._closeSubContainers(o.level + 2), i._updateItemRoles(o);
                            break;
                        case "checkMode":
                            o.itemContainer.setAttribute("check-mode", n), i._changeToRadioButtonMode(n, o.itemContainer, o), i._updateItemRoles(o);
                            break;
                        case "disabled":
                            {
                                if (Smart.ListMenu && i instanceof Smart.ListMenu) {
                                    if (i._view)
                                        for (; o.contains(i._view);) i._backButtonClickHandler()
                                } else i._isContainerOpened(o.container.level, o.container) && i._closeSubContainers(o.level + 1, o.container);
                                if (!o.checked) return;o.checked = !1;
                                const e = a.checkMode;
                                "radioButton" === e ? i._validateRadioButtonSelection(r, o.level, []) : "checkbox" !== e && i._refreshCheckableItems(a);
                                break
                            }
                        case "separator":
                            i._refreshCheckableItems(a)
                    }
                }
            }), Smart("smart-menu", class extends Smart.BaseElement {
                static get properties() { return { autoCloseDelay: { value: 100, type: "number" }, autoFocusOnMouseenter: { value: !1, type: "boolean" }, checkable: { value: !1, type: "boolean" }, checkboxes: { value: !1, type: "boolean" }, checkMode: { value: "checkbox", type: "string" }, closeAction: { value: "up", allowedValues: ["up", "down", "none"], type: "string" }, dataSource: { value: null, type: "array?", reflectToAttribute: !1 }, displayMember: { value: "label", type: "string" }, dropDownAppendTo: { value: null, type: "any?" }, dropDownOverlay: { value: !1, type: "boolean" }, dropDownPosition: { value: "auto", allowedValues: ["top-left", "top-right", "bottom-left", "bottom-right", "overlay-left", "overlay-right", "auto"], type: "string" }, enableMouseWheelAction: { value: !1, type: "boolean" }, innerHTML: { type: "string", reflectToAttribute: !1 }, itemsMember: { value: "items", type: "string" }, minimizeIconTemplate: { value: null, type: "string?" }, minimizeWidth: { value: null, type: "number?" }, mode: { value: "horizontal", allowedValues: ["horizontal", "vertical", "dropDown", "tree"], type: "string" }, opened: { value: !1, type: "boolean" }, overflow: { value: "auto", allowedValues: ["auto", "hidden", "scroll"], type: "string" }, preventCloseOnCheck: { value: !1, type: "boolean" }, selectionMode: { value: "click", allowedValues: ["click", "mouseenter"], type: "string" }, valueMember: { value: "value", type: "string" } } }
                static get listeners() { return { "container.click": "_selectionHandler", keydown: "_keydownHandler", mouseenter: "_mouseenterHandler", mouseleave: "_mouseleaveHandler", "container.mouseout": "_mouseoutMouseoverHandler", "container.mouseover": "_mouseoutMouseoverHandler", resize: "_resizeHandler", transitionend: "_transitionendHandler", "hamburgerIcon.click": "_hamburgerIconClickHandler", "mainContainer.click": "_mainContainerHandler", "mainContainer.mouseleave": "_mainContainerHandler", "mainContainer.mouseout": "_mainContainerHandler", "mainContainer.mouseover": "_mainContainerHandler", "document.down": "_documentDownHandler", "document.up": "_documentUpHandler" } }
                static get requires() { return { "Smart.RepeatButton": "smart.button.js" } }
                static get styleUrls() { return ["smart.button.css", "smart.menu.css"] }
                get items() { return this._menuItems }
                template() { return '<div id="container" role="presentation">\n                    <div id="minimizedHeader" class="smart-header smart-minimized-header smart-hidden" role="presentation">\n                        <div id="hamburgerIcon" class="smart-hamburger-icon smart-hidden" role="button" aria-label="Toggle minimized menu" aria-haspopup="true">\n                            <div id="hamburgerIconLineTop" class="smart-hamburger-icon-line smart-hamburger-icon-line-top" role="presentation"></div>\n                            <div id="hamburgerIconLineCenter" class="smart-hamburger-icon-line smart-hamburger-icon-line-center" role="presentation"></div>\n                            <div id="hamburgerIconLineBottom" class="smart-hamburger-icon-line smart-hamburger-icon-line-bottom" role="presentation"></div>\n                            <div id="customIconContainer" class="smart-hamburger-icon-custom-container smart-hidden" role="presentation"></div>\n                        </div>\n                    </div>\n                    <smart-repeat-button id="scrollButtonNear" class="smart-menu-scroll-button smart-spin-button smart-scroll-button-near smart-hidden" animation="[[animation]]" unfocusable right-to-left="[[rightToLeft]]">\n                        <div id="arrowNear" class="smart-arrow" aria-hidden="true"></div>\n                    </smart-repeat-button>\n                    <div id="mainContainer" class="smart-menu-main-container" role="presentation">\n                        <content></content>\n                    </div>\n                    <smart-repeat-button id="scrollButtonFar" class="smart-menu-scroll-button smart-spin-button smart-scroll-button-far smart-hidden" animation="[[animation]]" unfocusable right-to-left="[[rightToLeft]]">\n                        <div id="arrowFar" class="smart-arrow" aria-hidden="true"></div>\n                    </smart-repeat-button>\n                </div>' }
                attached() {
                    const e = this;
                    if (super.attached(), !e.isCompleted || !e.isRendered || "tree" === e._element || Smart.ListMenu && e instanceof Smart.ListMenu) return;
                    const t = e._scrollInfo;
                    if (null !== e.dropDownAppendTo) {
                        if (e._minimized) e._dropDownParent.appendChild(e.$.mainContainer);
                        else
                            for (let t = 0; t < e._containersInBody.length; t++) e._dropDownParent.appendChild(e._containersInBody[t]);
                        "dropDown" === e.mode && (e._dropDownParent === e.parentElement ? e._dynamicallyReparented ? delete e._dynamicallyReparented : e._positionRelativeTo = null : (e._positionRelativeTo = e.parentElement, e._dynamicallyReparented = !0, setTimeout((function() { e._dropDownParent.appendChild(e) }), 0)))
                    }
                    t && t.forEach((function(e, t) { t.scrollLeft = e.left, t.scrollTop = e.top }))
                }
                detached() {
                    const e = this;
                    super.detached(), "tree" === e._element || Smart.ListMenu && e instanceof Smart.ListMenu || (e._close(), null !== e.dropDownAppendTo && (e._minimized ? e._dropDownParent.removeChild(e.$.mainContainer) : e._removeContainersInBody()))
                }
                ready() { super.ready() }
                render() {
                    const e = this;
                    e._element = "menu", e._edgeMacFF = Smart.Utilities.Core.Browser.Edge || Smart.Utilities.Core.Browser.Firefox && -1 !== navigator.platform.toLowerCase().indexOf("mac"), e._containers = [], e._containersInBody = [], e._openedContainers = [], e._containersFixedHeight = [], e._menuItemsGroupsToExpand = [], e._additionalScrollButtons = [], e._scrollInfo = new Map, e._createElement(), super.render()
                }
                addItem(e, t) {
                    const n = this;
                    if (!(e instanceof Smart.MenuItem || e instanceof Smart.MenuItemsGroup))
                        if ("string" == typeof e) {
                            const t = document.createElement("smart-menu-item");
                            t.label = e, e = t
                        } else {
                            if (!e || !e.label) return; {
                                const t = document.createElement("smart-menu-item");
                                t.label = e.label, e = t
                            }
                        }
                    let o, i, r;
                    if (e.isDirty = !1, void 0 === t) o = n, i = 1, r = t = n.$.mainContainer;
                    else {
                        if ((t = n.getItem(t)) instanceof Smart.MenuItemsGroup == 0) return;
                        o = t, i = t.level + 1, r = t.itemContainer
                    }
                    if (n._createItemHTMLStructure(e, i, t, r.childElementCount, 0), e instanceof Smart.MenuItemsGroup && (n._processHTML(e, i + 1), n._checkContainersLength()), r.appendChild(e), n._checkOverflowAddRemove(e.level, r), e instanceof Smart.MenuItemsGroup && ("tree" === n.mode || n._minimized)) {
                        const t = e.getElementsByClassName("smart-menu-items-group-arrow");
                        for (let e = 0; e < t.length; e++) t[e].className = "smart-menu-items-group-arrow down smart-arrow-down";
                        n._expandItemsByDefault()
                    }
                    n._refreshCheckableItems(o)
                }
                checkItem(e) { void 0 === (e = this.getItem(e)) || e.checked || e.disabled || e.templateApplied || this._toggleItem(e) }
                clear() {
                    const e = this;
                    e.$.mainContainer.innerHTML = "", e._removeContainersInBody(), e._menuItems = {}, e._containers = [], e._containersInBody = [], e._openedContainers = [], e._containersFixedHeight = [], e._menuItemsGroupsToExpand = [], e._additionalScrollButtons = []
                }
                clickItem(e) { const t = this; "string" == typeof e && (e = t.getItem(e)), e && e.nodeName && t._selectionHandler({ type: "click", isTrusted: !0, target: e, stopPropagation: () => {}, preventDefault: () => {} }) }
                close() { const e = this; "dropDown" !== e.mode || !1 === e.opened && e.$.hasClass("smart-visibility-hidden") || (e.$.fireEvent("closing", arguments[0] || { trigger: "programmatic" }).defaultPrevented ? e.opened = !0 : (e.opened = !1, e.$.addClass("smart-visibility-hidden"), e._close(), e.$.fireEvent("close"))) }
                collapseItem(e, t) {
                    const n = this,
                        o = n.animation,
                        i = !1 === t && n.hasAnimation;
                    if (void 0 === e) return i && (n.animation = "none"), n._close(), void(i && setTimeout((function() { n.animation = o }), 0));
                    if (void 0 === (e = n.getItem(e)) || e instanceof Smart.MenuItem) return;
                    const r = e.level;
                    if (n._openedContainers[r + 1] && n._isContainerOpened(r + 1, e.container)) {
                        const t = n.mode;
                        i && (n.animation = "none"), n._closeSubContainers(r + 1, e.container, void 0, !1 !== arguments[2]), 1 !== r && "tree" !== t || n._checkOverflow(n.$.mainContainer, "horizontal" === t, [n.$.scrollButtonNear, n.$.scrollButtonFar]), i && (n.animation = o)
                    }
                }
                expandItem(e, t) {
                    const n = this;
                    if (void 0 === (e = n.getItem(e)) || e instanceof Smart.MenuItemsGroup && n._isContainerOpened(e.level + 1, e.container) && n._isBranchExpanded(e)) return;
                    void 0 !== Smart.Menu.processTimer && n._lazyInitItems();
                    const o = [e],
                        i = n.animation,
                        r = !1 === t && n.hasAnimation;
                    let a = e.parentItem;
                    for (r && (n.animation = "none"), n._discardKeyboardHover(); a;) o.unshift(a), a = a.parentItem;
                    for (let e = 0; e < o.length; e++) {
                        const t = o[e];
                        if (e === o.length - 1 && t instanceof Smart.MenuItem) { t.disabled || t.templateApplied || n._hoverViaKeyboard(t); break }
                        n._isContainerOpened(t.container.level, t.container) || n._menuItemsGroupSelectionHandler(t, { target: t, type: "expand", isTrusted: !0 }, arguments[2])
                    }
                    r && (n.animation = i)
                }
                getItem(e) {
                    const t = this;
                    let n;
                    if (null != e && t._menuItems) {
                        if ("string" == typeof e) { if (/^[0-9]*([.]?[0-9]*)*$/gm.test(e)) return t._menuItems[e]; if (n = t.$.mainContainer.querySelector('[id="' + e + '"]'), null === n) return t._menuItems[e] } else {
                            if (!isNaN(e)) return t._menuItems[e.toString()];
                            n = e
                        }
                        if ((n instanceof Smart.MenuItem || n instanceof Smart.MenuItemsGroup) && (t.contains(n) || t.$.mainContainer.contains(n) || n.parentElement.parentElement.ownerElement === t)) return n
                    }
                }
                maximize() {
                    const e = this;
                    if (!e._minimized) return;
                    const t = e.animation;
                    if (e.$.mainContainer.style.marginTop = "", e.$.mainContainer.style.marginLeft = "", e.enableShadowDOM && !e.$.mainContainer.id && (e.$.mainContainer.id = e.$.mainContainer.getAttribute("smart-id")), "none" !== t && (e.animation = "none"), e._positionDetection.removeOverlay(), e._closeSubContainers(2), e.$minimizedHeader.addClass("smart-hidden"), e._minimized = !1, e._minimizedDropDownOpened && (e.$hamburgerIcon.removeClass("smart-close-button"), e._minimizedDropDownOpened = !1), null !== e.dropDownAppendTo && e._appendMinimizedContainerToMenu(e.$.mainContainer, e.$.scrollButtonFar), "tree" !== e.mode) {
                        e.$mainContainer.addClass("smart-menu-main-container"), e.$mainContainer.removeClass("smart-menu-minimized-items-container");
                        const t = e.$.mainContainer.getElementsByClassName("smart-menu-items-group-arrow");
                        for (let n = 0; n < t.length; n++) e._setArrowDirection(t[n], t[n].parentElement.parentElement.level + 1);
                        null !== e.dropDownAppendTo && e._moveDropDownsToExternalContainer(), e._applyContainerFixedHeight()
                    }
                    e.$mainContainer.removeClass("smart-visibility-hidden"), e.$hamburgerIcon.addClass("smart-hidden"), e.removeAttribute("minimized"), e._checkOverflow(e.$.mainContainer, "horizontal" === e.mode, [e.$.scrollButtonNear, e.$.scrollButtonFar]), "none" !== t && setTimeout((function() { e.animation = t }), 0), e.$.mainContainer.removeAttribute("drop-down"), e.$.hamburgerIcon.removeAttribute("aria-expanded"), e.$.hamburgerIcon.removeAttribute("aria-owns"), e.$.mainContainer.setAttribute("role", "presentation"), e.$.mainContainer.removeAttribute("aria-orientation"), e.setAttribute("role", "menu"), e.setAttribute("aria-orientation", "horizontal" === e.mode ? "horizontal" : "vertical")
                }
                minimize() {
                    const e = this;
                    if (e._minimized || "dropDown" === e.mode) return;
                    e.$minimizedHeader.removeClass("smart-hidden");
                    const t = null !== e.dropDownAppendTo,
                        n = e.animation,
                        o = e.hasAnimation;
                    if (o && (e.animation = "none"), e._positionDetection.removeOverlay(), e._closeSubContainers(2), o && t && (e.animation = n), "tree" !== e.mode && (t && e._moveDropDownsToMenu(), e._removeContainerFixedHeight()), e._hideMainContainerScrollButtons(), e.$mainContainer.removeClass("smart-menu-main-container"), e.$mainContainer.addClass("smart-visibility-hidden"), e.enableShadowDOM && e.$.mainContainer.removeAttribute("id"), e._edgeMacFF && (e.$.mainContainer.style.left = "", e.$.mainContainer.style.top = "", e.$mainContainer.addClass("not-in-view")), e.$hamburgerIcon.removeClass("smart-hidden"), t && e._appendMinimizedContainerToExternalElement(e.$.mainContainer), setTimeout((function() { e.$mainContainer.addClass("smart-menu-minimized-items-container"), o && !t && (e.animation = n) }), 0), e._minimized = !0, e.setAttribute("minimized", ""), "tree" !== e.mode)
                        for (let t = 0; t < e._containers.length; t++) {
                            const n = e._containers[t];
                            n.level > 2 && e._setArrowDirection(n.menuItemsGroup.children[0].children[1], n.level)
                        }
                    e.$.mainContainer.setAttribute("drop-down", ""), e.setAttribute("role", "presentation"), e.removeAttribute("aria-orientation"), e.$.hamburgerIcon.setAttribute("aria-expanded", !1), e.$.hamburgerIcon.setAttribute("aria-owns", e.$.mainContainer.id), e.$.mainContainer.setAttribute("role", "menu"), e.$.mainContainer.setAttribute("aria-orientation", "vertical")
                }
                open(e, t) {
                    const n = this;
                    if ("dropDown" !== n.mode) return;
                    if (n.$.fireEvent("opening").defaultPrevented) return void(n.opened = !1);
                    let o;
                    if (n.opened = !0, n._positionRelativeTo) {
                        const i = n._positionRelativeTo.getBoundingClientRect();
                        e += i.left, t += i.top, n._positionedParent ? (o = n._positionedParent.getBoundingClientRect(), e -= o.left, t -= o.top) : (e += window.pageXOffset, t += window.pageYOffset)
                    }
                    let i = e + n.offsetWidth - document.documentElement.clientWidth,
                        r = t + n.offsetHeight - document.documentElement.clientHeight;
                    o ? (i += o.left, r += o.top) : (i -= window.pageXOffset, r -= window.pageYOffset), i > 0 ? e -= i : e = o ? Math.max(e, -o.left) : Math.max(e, window.pageXOffset), r > 0 ? t -= r : t = o ? Math.max(t, -o.top) : Math.max(t, window.pageYOffset), n.style.right = "", isNaN(e) || (n.rightToLeft && (n.style.right = "initial"), n.style.left = e + "px"), isNaN(t) || (n.style.top = t + "px"), n.$.removeClass("smart-visibility-hidden"), n.$.fireEvent("open"), n.hasAnimation || (n._checkOverflowOnOpen && (n._checkOverflow(n.$.mainContainer, !1, [n.$.scrollButtonNear, n.$.scrollButtonFar]), delete n._checkOverflowOnOpen), n._noAutoFocus || n.focus())
                }
                removeItem(e) {
                    const t = this;
                    if (void 0 === (e = t.getItem(e))) return;
                    const n = e.parentElement,
                        o = e.parentItem || t;
                    if (e instanceof Smart.MenuItemsGroup) { const n = e.container; if (t._isContainerOpened(n.level, n) && t._closeSubContainers(n.level, n), 1 === e.level) { const e = t._containersInBody.indexOf(n); - 1 !== e && (t._containersInBody.splice(e, 1), null === t.dropDownAppendTo || "tree" === t.mode || t._minimized || t._dropDownParent.removeChild(n)) } }
                    n.removeChild(e), t._refreshContainersArrays(), t._menuItems = {}, t._refreshItemPaths(t.$.mainContainer, !0), t._checkOverflowAddRemove(e.level, n), t._refreshCheckableItems(o)
                }
                uncheckItem(e) { void 0 === (e = this.getItem(e)) || !e.checked || e.disabled || e.templateApplied || this._toggleItem(e) }
                propertyChangedHandler(e, t, n) {
                    super.propertyChangedHandler(e, t, n);
                    const o = this;
                    if ("tree" !== o._element) switch (e) {
                        case "animation":
                            o.$.mainContainer.setAttribute("animation", n), o._additionalScrollButtons.forEach((function(e) { e[0].animation = n, e[1].animation = n })), null !== o._dropDownParent && o._containers.forEach((function(e) { e.setAttribute("animation", n) }));
                            break;
                        case "checkable":
                            "tree" === o.mode || o._minimized ? o._minimized && null !== o.dropDownAppendTo && r("checkable", o.$.mainContainer, n) : o._closeSubContainers(2), o._updateItemRoles(o);
                            break;
                        case "checkboxes":
                            if (o._close(), null !== o.dropDownAppendTo) {
                                for (let e = 0; e < o._containers.length; e++) r("checkboxes", o._containers[e], n);
                                o._minimized && r("checkboxes", o.$.mainContainer, n)
                            }
                            o._updateItemRoles();
                            break;
                        case "checkMode":
                            o._changeToRadioButtonMode(n, o.$.mainContainer), o._minimized && null !== o.dropDownAppendTo && o.$.mainContainer.setAttribute("check-mode", n), o._updateItemRoles(o);
                            break;
                        case "dataSource":
                            { let e = !1;o._minimized && (o.maximize(), e = !0), o._removeContainersInBody(), o._containersInBody = [], o._menuItems = {}, o._processDataSource(), o._checkContainersLength(), e ? o.minimize() : i(), o._expandItemsByDefault(), o._refreshCheckableItems(), o._suppressResizeHandler = !0, setTimeout((() => delete o._suppressResizeHandler), 500); break }
                        case "innerHTML":
                            o.$.mainContainer.innerHTML = n, o._lazyInitItems();
                            break;
                        case "dropDownAppendTo":
                            {
                                const e = o._dropDownParent;
                                if (o._positionDetection.getDropDownParent(), o._dropDownParent === e || "tree" === o.mode && !o._minimized) return;
                                if (o._close(), o._minimized) return void(null === n ? o._appendMinimizedContainerToMenu(o.$.mainContainer, o.$.scrollButtonFar) : o._appendMinimizedContainerToExternalElement(o.$.mainContainer));
                                if (null !== o._dropDownParent && null === e) o._moveDropDownsToExternalContainer();
                                else if (null === o._dropDownParent && null !== e) o._moveDropDownsToMenu();
                                else if (null !== o._dropDownParent && null !== e)
                                    for (let e = 0; e < o._containersInBody.length; e++) o._dropDownParent.appendChild(o._containersInBody[e]);null !== n || o.$mainContainer.hasClass("simple") ? o._checkOverflow(o.$.mainContainer, "horizontal" === o.mode, [o.$.scrollButtonNear, o.$.scrollButtonFar]) : o._hideMainContainerScrollButtons();
                                for (let e = 0; e < o._containersFixedHeight.length; e++) o._containersFixedHeight[e].itemContainer.checkOverflow = !0;
                                "dropDown" === o.mode && (o.close({ trigger: "internal" }), o._reparentMenu(!0, e));
                                break
                            }
                        case "dropDownOverlay":
                            n || o._positionDetection.removeOverlay();
                            break;
                        case "disabled":
                            n && o._close(), o._setFocusable(), o.$.scrollButtonNear.disabled = n, o.$.scrollButtonFar.disabled = n, n || null === o.dropDownAppendTo && !o.$mainContainer.hasClass("simple") && "tree" !== o.mode || o._updateScrollButtonVisibility(o.$.mainContainer, "horizontal" === o.mode, [o.$.scrollButtonNear, o.$.scrollButtonFar]);
                            break;
                        case "dropDownPosition":
                        case "mode":
                            {
                                if ("mode" === e) {
                                    if (delete o._dynamicallyReparented, "tree" === t || o._minimized ? (o._closeSubContainersTreeMode(2, void 0, void 0, void 0, !0), o._openedContainers = []) : o._closeSubContainersDefaultMode(2), o._discardKeyboardHover(!0), o._minimized && o._minimizedDropDownOpened && (o.$mainContainer.addClass("smart-visibility-hidden"), o.$hamburgerIcon.removeClass("smart-close-button"), o.$.hamburgerIcon.setAttribute("aria-expanded", !1), o._minimizedDropDownOpened = !1), "horizontal" !== n && "horizontal" !== t || o._changeScrollButtonsArrows(), o._minimized) return void("dropDown" === n && (o.mode = t));
                                    o.setAttribute("aria-orientation", "horizontal" === o.mode ? "horizontal" : "vertical"), !1 === o.opened && ("dropDown" === n ? o.$.addClass("smart-visibility-hidden") : "dropDown" === t && o.$.removeClass("smart-visibility-hidden")), "tree" === t ? (null !== o.dropDownAppendTo && o._moveDropDownsToExternalContainer(), o.$mainContainer.addClass("smart-menu-main-container"), o.$mainContainer.removeClass("smart-menu-minimized-items-container"), o._applyContainerFixedHeight()) : "tree" === n && (null !== o.dropDownAppendTo && o._moveDropDownsToMenu(), o._applyTreeMode()), "auto" === o.overflow && o._hideMainContainerScrollButtons(), i()
                                }
                                if ("tree" === o.mode || o._minimized) return o._minimizedDropDownOpened && o._close(), void(o._minimized && null !== o.dropDownAppendTo && o.$.mainContainer.setAttribute(o.properties[e].attributeName, n));
                                "dropDownPosition" === e && o._close();
                                const r = o._containers.map((e => e.menuItemsGroup));
                                for (let e = 0; e < r.length; e++) {
                                    const t = r[e];
                                    o._setArrowDirection(t.children[0].children[1], t.level + 1)
                                }
                                if (null !== o.dropDownAppendTo)
                                    for (let t = 0; t < o._containers.length; t++) {
                                        const i = o._containers[t];
                                        i.setAttribute(Smart.Utilities.Core.toDash(e), n), i.level > 2 && o._setArrowDirection(i.menuItemsGroup.children[0].children[1], i.level)
                                    }
                                break
                            }
                        case "minimizeIconTemplate":
                            o._applyMinimizeIconTemplate(n, t);
                            break;
                        case "minimizeWidth":
                            o._resizeHandler();
                            break;
                        case "opened":
                            n ? o.open() : o.close({ trigger: "internal" });
                            break;
                        case "overflow":
                            o._handleOverflowChange();
                            break;
                        case "rightToLeft":
                            if ("tree" !== o.mode) {
                                const e = o._containers.map((e => e.menuItemsGroup));
                                for (let t = 0; t < e.length; t++) {
                                    const n = e[t];
                                    o._setArrowDirection(n.children[0].children[1], n.level + 1)
                                }
                                if (null !== o.dropDownAppendTo) {
                                    n ? o.$.mainContainer.setAttribute("right-to-left", "") : o.$.mainContainer.removeAttribute("right-to-left");
                                    for (let e = 0; e < o._containers.length; e++) {
                                        const t = o._containers[e];
                                        n ? t.setAttribute("right-to-left", "") : t.removeAttribute("right-to-left"), t.level > 2 && o._setArrowDirection(t.menuItemsGroup.children[0].children[1], t.level)
                                    }
                                }
                            }
                            break;
                        case "theme":
                            if (null === o.dropDownAppendTo || Smart.ListMenu && o instanceof Smart.ListMenu) return;
                            if (o._minimized) "" !== t && o.$mainContainer.removeClass(t), "" !== n && o.$mainContainer.addClass(n);
                            else
                                for (let e = 0; e < o._containers.length; e++) { const i = o._containers[e]; "" !== t && i.classList.remove(t), "" !== n && i.classList.add(n) }
                            break;
                        case "unfocusable":
                            o._setFocusable()
                    }

                    function i() { null === o.dropDownAppendTo && "tree" !== o.mode || o._checkOverflow(o.$.mainContainer, "horizontal" === o.mode, [o.$.scrollButtonNear, o.$.scrollButtonFar]) }

                    function r(e, t, n) { n ? t.setAttribute(e, "") : t.removeAttribute(e) }
                }
                _addOpenedContainer(e, t) {
                    const n = this;
                    if ("tree" === n.mode || n._minimized) { n._openedContainers[e] || (n._openedContainers[e] = []); const o = t.menuItemsGroup; return o.set("expanded", !0), o.setAttribute("aria-expanded", !0), n._updateState && n._updateState("expanded", o.id, !0), n._openedContainers[e].push(t) }
                    n._openedContainers[e] = t
                }
                _appendMinimizedContainerToExternalElement(e) {
                    const t = this;
                    e.ownerElement = t, t._dropDownParent.appendChild(e), e.setAttribute("animation", t.animation), "" !== t.theme && e.$.addClass(t.theme), e.$.addClass("smart-menu-drop-down smart-drop-down"), e.$.addClass("smart-drop-down-repositioned"), e.setAttribute("check-mode", t.checkMode), e.setAttribute("drop-down-position", t.dropDownPosition), e.setAttribute("mode", t.mode), e.setAttribute("loading-indicator-position", t.loadingIndicatorPosition), t.rightToLeft && e.setAttribute("right-to-left", ""), t.checkable && e.setAttribute("checkable", ""), t.checkboxes && e.setAttribute("checkboxes", ""), t.$.view && t.detachedChildren.indexOf(t.$.view) && t.detachedChildren.push(t.$.view)
                }
                _appendMinimizedContainerToMenu(e, t) {
                    const n = this;
                    delete e.ownerElement, n.$.container.insertBefore(e, t), e.removeAttribute("animation"), "" !== n.theme && e.$.removeClass(n.theme), e.$.removeClass("smart-menu-drop-down smart-drop-down"), e.$.removeClass("smart-drop-down-repositioned"), e.removeAttribute("checkable"), e.removeAttribute("checkboxes"), e.removeAttribute("check-mode"), e.removeAttribute("drop-down-position"), e.removeAttribute("mode"), e.removeAttribute("loading-indicator-position"), e.removeAttribute("style"), e.removeAttribute("right-to-left")
                }
                _applyContainerFixedHeight() { const e = this; for (let t = 0; t < e._containers.length; t++) { const n = e._containers[t]; - 1 !== e._containersFixedHeight.indexOf(n) ? (n.style.height = n.menuItemsGroup.dropDownHeight + "px", n.itemContainer.checkOverflow = !0) : n.style.height = "" } }
                _applyGrouping(e, t) {
                    const n = this;
                    let o;
                    o = e === n.$.mainContainer ? Array.from(e.children) : Array.from(e.container.firstElementChild.children);
                    for (let e = 0; e < o.length; e++) {
                        const i = o[e];
                        i.originalIndex = e, i instanceof Smart.MenuItemsGroup && void 0 === t && n._applyGrouping(i)
                    }
                    n._sortItems(e)
                }
                _applyMinimizeIconTemplate(e, t) {
                    const n = this;
                    if (null === e) {
                        if (null === t) return;
                        n.$customIconContainer.addClass("smart-hidden"), n.$.customIconContainer.innerHTML = "", n.$hamburgerIconLineTop.removeClass("smart-hidden"), n.$hamburgerIconLineCenter.removeClass("smart-hidden"), n.$hamburgerIconLineBottom.removeClass("smart-hidden")
                    } else {
                        const o = document.getElementById(e);
                        if (null !== o && "template" === o.tagName.toLowerCase()) {
                            const e = document.importNode(o.content, !0);
                            n.$hamburgerIconLineTop.addClass("smart-hidden"), n.$hamburgerIconLineCenter.addClass("smart-hidden"), n.$hamburgerIconLineBottom.addClass("smart-hidden"), n.$.customIconContainer.innerHTML = "", n.$.customIconContainer.appendChild(e), n.$customIconContainer.removeClass("smart-hidden")
                        } else n.minimizeIconTemplate = t
                    }
                }
                _applyTreeMode() {
                    const e = this,
                        t = e.$.mainContainer.getElementsByClassName("smart-menu-items-group-arrow");
                    if (e.$mainContainer.removeClass("smart-menu-main-container"), e.$mainContainer.addClass("smart-menu-minimized-items-container"), e.isCompleted && e.isRendered)
                        for (let e = 0; e < t.length; e++) t[e].className = "smart-menu-items-group-arrow down";
                    e._removeContainerFixedHeight()
                }
                _arrowLeftHandler(e, t, n, o) {
                    const i = this;
                    1 === e ? "horizontal" === t && i._levelOneNavigate("_getLastEnabledChild", n, o) : 2 === e ? i._levelOneNavigateFromLowerLevel("_getPreviousEnabledChild", n) : i._escapeHandler(n, e, o)
                }
                _arrowRightHandler(e, t, n, o) {
                    const i = this;
                    1 === e ? "horizontal" === t ? i._levelOneNavigate("_getFirstEnabledChild", n, o) : i._levelOneOpenDropDown(n) : n instanceof Smart.MenuItemsGroup ? i._selectionHandler({ target: n, isTrusted: !0 }) : i._levelOneNavigateFromLowerLevel("_getNextEnabledChild", n)
                }
                _browserBoundsDetection(e) {
                    const t = this;
                    if ("tree" === t.mode && !t._minimized) return;
                    if (e.style.marginTop = "", e.style.marginLeft = "", "auto" !== t.dropDownPosition) return;
                    const n = 1 === window.devicePixelRatio ? document.documentElement.clientWidth : window.innerWidth,
                        o = 1 === window.devicePixelRatio ? document.documentElement.clientHeight : window.innerHeight,
                        i = e.getBoundingClientRect(),
                        r = n - i.left - e.offsetWidth,
                        a = o - i.top - e.offsetHeight;
                    r < 10 && (e.style.marginLeft = Math.min(r - 10, -10) + "px"), a < 10 && (e.style.marginTop = Math.min(a - 10, -10) + "px")
                }
                _changeScrollButtonsArrows() { const e = this; "horizontal" === e.mode ? (e.$.scrollButtonNear.setAttribute("aria-label", "Scroll left"), e.$.scrollButtonFar.setAttribute("aria-label", "Scroll right"), e.$arrowNear.removeClass("smart-arrow-up"), e.$arrowFar.removeClass("smart-arrow-down"), e.$arrowNear.addClass("smart-arrow-left"), e.$arrowFar.addClass("smart-arrow-right")) : (e.$.scrollButtonNear.setAttribute("aria-label", "Scroll up"), e.$.scrollButtonFar.setAttribute("aria-label", "Scroll down"), e.$arrowNear.removeClass("smart-arrow-left"), e.$arrowFar.removeClass("smart-arrow-right"), e.$arrowNear.addClass("smart-arrow-up"), e.$arrowFar.addClass("smart-arrow-down")) }
                _changeToRadioButtonMode(e, t, n) {
                    if ("radioButton" === e) {
                        const e = [];
                        for (let n = 0; n < t.childElementCount; n++) { const o = t.children[n];!o.checked || o.disabled || o.templateApplied || e.push(o) }
                        this._validateRadioButtonSelection(n, n ? n.level + 1 : 1, e)
                    }
                }
                _checkContainersLength(e) {
                    const t = this;
                    0 === t._containers.length ? (t.$mainContainer.addClass("simple"), e || t._checkOverflow(t.$.mainContainer, "horizontal" === t.mode, [t.$.scrollButtonNear, t.$.scrollButtonFar])) : e || (t.$mainContainer.removeClass("simple"), null === t.dropDownAppendTo && "tree" !== t.mode && t.$mainContainer.removeClass("scroll-buttons-shown one-button-shown"))
                }
                _checkOverflow(e, t, n) {
                    const o = this,
                        i = o.$.mainContainer,
                        r = e === i ? o.overflow : "auto";
                    if (o._minimized || "hidden" === r || null === o.dropDownAppendTo && "tree" !== o.mode && e === i && !i.classList.contains("simple")) return;
                    if ("dropDown" === o.mode && !o.opened) return void(o._checkOverflowOnOpen = !0);
                    const a = e.scrollLeft,
                        s = a / (e.scrollWidth - e.offsetWidth),
                        l = e.scrollTop,
                        d = l / (e.scrollHeight - e.offsetHeight);
                    let m, c, u;
                    "auto" === r && (e.classList.remove("scroll-buttons-shown"), e.classList.remove("one-button-shown"), n[0].$.addClass("smart-hidden"), n[1].$.addClass("smart-hidden")), t ? (m = Math.round(e.scrollWidth) > Math.round(e.offsetWidth), c = s > 0, u = s < 1) : (m = Math.round(e.scrollHeight) > Math.round(e.offsetHeight), c = d > 0, u = d < 1), m ? "auto" === r ? (e.classList.add("scroll-buttons-shown"), c && n[0].$.removeClass("smart-hidden"), u && n[1].$.removeClass("smart-hidden"), !1 === (c && u) && e.classList.add("one-button-shown"), o.disabled || (n[0].disabled = !1, n[1].disabled = !1), e.scrollLeft = a, e.scrollTop = l) : (n[0].$.removeClass("smart-hidden"), n[1].$.removeClass("smart-hidden"), o.disabled ? (n[0].disabled = !0, n[1].disabled = !0) : (n[0].disabled = !c, n[1].disabled = !u)) : "scroll" === r && (n[0].disabled = !0, n[1].disabled = !0), e === i && "tree" !== o.mode && o._close(), o._scrollInfo.set(e, { left: e.scrollLeft, top: e.scrollTop })
                }
                _checkOverflowAddRemove(e, t) {
                    const n = this;
                    1 === e && null !== n.dropDownAppendTo || "tree" === n.mode ? n._checkOverflow(n.$.mainContainer, "horizontal" === n.mode, [n.$.scrollButtonNear, n.$.scrollButtonFar]) : e > 1 && t.dropDownHeightSet && (n._isContainerOpened(e, t.container) ? n._checkOverflow(t, !1, [t.container.children[0], t.container.children[2]]) : t.checkOverflow = !0)
                }
                _close() {
                    const e = this;
                    e._positionDetection.removeOverlay(), e._closeSubContainers(2), e._discardKeyboardHover(!0), e._minimized && e._minimizedDropDownOpened && (e.$mainContainer.addClass("smart-visibility-hidden"), e._edgeMacFF && (e.$.mainContainer.style.left = "", e.$.mainContainer.style.top = "", e.$mainContainer.addClass("not-in-view")), e.$hamburgerIcon.removeClass("smart-close-button"), e.$.hamburgerIcon.setAttribute("aria-expanded", !1), e._minimizedDropDownOpened = !1)
                }
                _closeSubContainers(e, t, n, o) { const i = this; "tree" === i.mode || i._minimized ? i._closeSubContainersTreeMode(e, t, n, o) : i._closeSubContainersDefaultMode(e, t, n) }
                _closeSubContainersDefaultMode(e, t, n) {
                    const o = this,
                        i = o._openedContainers;

                    function r(t) {
                        const r = i[t].menuItemsGroup;
                        n && t === e || (r.$.removeClass("focus"), r.removeAttribute("focus"), r.$.removeClass("hover"), r.removeAttribute("hover")), r.$.removeClass("smart-menu-items-group-opened"), r.$.removeClass("smart-menu-items-group-expanded"), r.setAttribute("aria-expanded", !1), i[t].$.addClass("smart-visibility-hidden"), o._edgeMacFF && 2 === t && !o.hasAnimation && (i[t].style.left = "", i[t].style.top = "", i[t].$.addClass("not-in-view")), o._minimized && o._browserBoundsDetection(o.$.mainContainer), o.$.fireEvent("collapse", { item: r, label: r.label, path: r.path, value: r.value, children: r.itemContainer.children }), i[t] = void 0
                    }
                    for (let t = i.length - 1; t >= e; t--) void 0 !== i[t] && r(t)
                }
                _closeSubContainersTreeMode(e, t, n, o, i) {
                    const r = this;
                    if (o) { const e = t.menuItemsGroup; if (r.$.fireEvent("collapsing", { item: e, label: e.label, path: e.path, value: e.value, children: t.itemContainer.children }).defaultPrevented) return }
                    if (void 0 === t) return void r._collapseAll(!1, i);
                    const a = t.menuItemsGroup;
                    if (a.set("expanded", !1), a.setAttribute("aria-expanded", !1), "menu" === r._element)
                        if (n) {
                            const e = r.$.mainContainer.getElementsByClassName("focus")[0];
                            e && (e.$.removeClass("focus"), e.removeAttribute("focus")), a.$.addClass("focus"), a.setAttribute("focus", ""), r._focusedViaKeyboard = a
                        } else a.$.removeClass("focus"), a.removeAttribute("focus");
                    else r._updateState("expanded", a.id, !1);
                    if (a.$.removeClass("smart-" + r._element + "-items-group-opened"), i || !r.hasAnimation ? (a.$.removeClass("smart-" + r._element + "-items-group-expanded"), a.setAttribute("aria-expanded", !1), t.$.addClass("smart-visibility-hidden"), r._minimized && r._browserBoundsDetection(r.$.mainContainer)) : r._collapseSection(t), o) {
                        const e = { item: a, label: a.label, path: a.path, value: a.value, children: a.itemContainer.children };
                        r.toggleCallback ? (e.type = "collapse", r.toggleCallback(e)) : r.$.fireEvent("collapse", e)
                    }
                    if (!r._openedContainers[e]) return;
                    const s = r._openedContainers[e].indexOf(t); - 1 !== s && r._openedContainers[e].splice(s, 1)
                }
                _collapseAll(e, t) {
                    const n = this;
                    for (let o = n._openedContainers.length - 1; o >= 2 && void 0 !== n._openedContainers[o]; o--)
                        for (let i = n._openedContainers[o].length - 1; i >= 0; i--) n._closeSubContainersTreeMode(o, n._openedContainers[o][i], void 0, e, t);
                    n.hasAnimation || n._checkOverflow(n.$.mainContainer, !1, [n.$.scrollButtonNear, n.$.scrollButtonFar]);
                    for (let e = n._openedContainers.length - 1; e >= 2; e--) {
                        const t = n._openedContainers[e];
                        if (void 0 !== t && 0 !== t.length) break;
                        n._openedContainers.splice(e, 1)
                    }
                    2 === n._openedContainers.length && (n._openedContainers = [])
                }
                _collapseSection(e) {
                    const t = this,
                        n = e.scrollHeight + "px";
                    t._treeAnimationInProgress = e, e.style.transition = "none", requestAnimationFrame((function() { "tree" === t.mode || t._minimized ? (e.style.height = n, e.style.transition = "", requestAnimationFrame((function() { e.style.height = "0px", "smart-tree" === t.tagName.toLowerCase() && e.$.addClass("smart-visibility-hidden"), "0px" === n && t._transitionendHandlerCollapse(t, e) }))) : e.style.transition = "" })), e.addEventListener("transitionend", t._transitionendHandlerCollapse)
                }
                _createElement() {
                    const e = this,
                        t = e.mode;
                    e.setAttribute("role", "menu"), e.$.mainContainer.id = e.id + "MainContainer", e.setAttribute("aria-orientation", "horizontal" === e.mode ? "horizontal" : "vertical"), e._positionDetection = new Smart.Utilities.PositionDetection(e), e._positionDetection.getDropDownParent(), e._reparentMenu(), e.disabled && (e.$.scrollButtonNear.disabled = !0, e.$.scrollButtonFar.disabled = !0), null === e.dataSource && e.$.mainContainer.firstElementChild instanceof HTMLUListElement && e._processUList();
                    const n = (e.shadowRoot || e).querySelectorAll("smart-menu-item, smart-menu-items-group"),
                        o = function() {
                            const n = e.animation;
                            e._changeScrollButtonsArrows(), e._setFocusable(), "dropDown" === t && !1 === e.opened && (e.hasAnimation ? (e.animation = "none", e.$.addClass("smart-visibility-hidden"), e.animation = n) : e.$.addClass("smart-visibility-hidden")), e._menuItems = {}, e.$.mainContainer.setAttribute("animation", n), null === e.dataSource ? e._processHTML(e.$.mainContainer, 1) : e._processDataSource(), e._checkContainersLength(!0), null === e.dropDownAppendTo && !e.$mainContainer.hasClass("simple") && "tree" !== e.mode || "scroll" !== e.overflow || (e.$mainContainer.addClass("scroll-buttons-shown"), e.$scrollButtonNear.removeClass("smart-hidden"), e.$scrollButtonFar.removeClass("smart-hidden"), e._updateScrollButtonVisibility(e.$.mainContainer, "horizontal" === t, [e.$.scrollButtonNear, e.$.scrollButtonFar])), e._applyMinimizeIconTemplate(e.minimizeIconTemplate, null), "tree" === t && e._applyTreeMode(), null !== e.minimizeWidth && e.offsetWidth <= e.minimizeWidth ? e.minimize() : e._checkOverflow(e.$.mainContainer, "horizontal" === t, [e.$.scrollButtonNear, e.$.scrollButtonFar]), e._expandItemsByDefault(), e._refreshCheckableItems(), e.__onCompleted && (e._onCompleted = e.__onCompleted, e.__onCompleted = null, e._onCompleted())
                        };
                    0 === n.length || e.enableShadowDOM || e.isInShadowDOM ? o() : (e._onCompleted && (e.__onCompleted = e._onCompleted, e._onCompleted = null), e._ensureItemsReady(n, o))
                }
                _ensureItemsReady(e, t) {
                    const n = this,
                        o = function() {
                            const n = function(t) { for (let n = 0; n < e.length; n++) e[n].context = "node" === t ? e[n] : document };
                            n("node"), t(), n()
                        };
                    if (0 === e.length) o();
                    else {
                        n._nodesReadyListeners = 0;
                        for (let t = 0; t < e.length; t++) {
                            const i = e[t],
                                r = function() {
                                    const e = n.context;
                                    n.context = n, n._nodesReadyListeners--, 0 === n._nodesReadyListeners && (o(), delete n._nodesReadyListeners), n.context = e
                                }.bind(n);
                            i.isCompleted || (n._nodesReadyListeners++, i.completeHandlers = [], i._onCompleted = r)
                        }
                        0 === n._nodesReadyListeners && o()
                    }
                }
                _createItemHTMLStructure(e, t, n, o) {
                    const i = this,
                        r = "smart-" + i._element + "-item-label-container",
                        a = "smart-" + i._element + "-item-label-element",
                        s = document.createDocumentFragment(),
                        l = e.children;
                    let d, m, c, u;
                    for (let e = 0; e < l.length; e++) { const t = l[e]; if (t.classList && (t.classList && t.classList.contains(r) ? d = t : t.classList && t.classList.contains(a) && (m = t), d && m)) break }
                    if (d) {
                        const t = d.querySelector("." + a);
                        if (null !== t) {
                            e.insertBefore(t.firstElementChild, e.children[0]);
                            const n = "smart-" + i._element + "-drop-down",
                                o = "smart-" + i._element + "-item-container",
                                r = e.querySelector("." + n);
                            if (r) {
                                const t = e.querySelector("." + o);
                                for (; t.childNodes.length;) e.appendChild(t.firstChild);
                                r.remove()
                            }
                        }
                        d.remove()
                    }
                    m && m.remove(), d = document.createElement("div"), m = document.createElement("div");
                    let p = document.createElement("span");
                    e.menu = i, t > 1 ? (e.originalIndex = o, c = n.path + "." + e.originalIndex, e.parentItem = n, u = n) : (e.originalIndex = o, c = "" + o, u = i), i.checkboxes && u.checkable && ("checkbox" === u.checkMode ? e.setAttribute("role", "menuitemcheckbox") : "radioButton" === u.checkMode && e.setAttribute("role", "menuitemradio")), e.path = c, i._menuItems[c] = e, d.className = r, m.className = a, "tree" === i._element && i._setIndentation(d, t, i.rightToLeft ? "paddingRight" : "paddingLeft");
                    const h = Array.from(e.childNodes);
                    for (let e = 0; e < h.length; e++) {
                        const t = h[e];
                        if (t instanceof Smart.MenuItem || t instanceof Smart.MenuItemsGroup) break;
                        p.appendChild(t)
                    }
                    if ("" === p.innerHTML.trim()) {
                        const t = e.label || e.getAttribute("label");
                        t && "" !== t ? i._setLabel(t, p, e, !0) : (e.set("label", "Item " + o), p.innerHTML = "Item " + o)
                    } else e.set("label", p.innerHTML.trim());
                    if (e.setAttribute("aria-label", e.label), e instanceof Smart.MenuItemsGroup && void 0 === e.titleLabel && (e.titleLabel = e.label), m.appendChild(p), s.appendChild(m), e.set("level", t), e.set("shortcut", e.shortcut || e.getAttribute("shortcut") || ""), e.shortcut && e instanceof Smart.MenuItem) {
                        const t = document.createElement("div");
                        t.id = e.id + "Shortcut", t.className = "smart-" + i._element + "-item-shortcut", t.innerHTML = e.shortcut, s.appendChild(t), e.setAttribute("aria-describedby", t.id)
                    }
                    d.appendChild(s), e.insertBefore(d, e.children[0]), e.id || (e.id = i.id + "ItemP" + e.path.replace(/\./g, "_") + "L" + e.label.replace(/[^a-zA-Z0-9\-\_]/g, ""))
                }
                _createMenuItemsGroupContainer(e, t) {
                    const n = this,
                        o = e.children,
                        i = "smart-" + n._element + "-drop-down",
                        r = "smart-" + n._element + "-item-container";
                    let a, s;
                    for (let e = 0; e < o.length; e++) { const t = o[e]; if (t.classList && (t.classList && t.classList.contains(i) ? a = t : t.classList && t.classList.contains(r) && (s = t), a && s)) break }
                    if (a || (a = document.createElement("div")), s || (s = document.createElement("div")), a.innerHTML = s.innerHTML = "", a.id = e.id + "Container", a.className = "smart-" + n._element + "-drop-down smart-visibility-hidden", n._edgeMacFF && 2 === t && "tree" !== n.mode && (a.className += " not-in-view"), a.$ || (a.$ = Smart.Utilities.Extend(a)), a.level = t, a.setAttribute("level", t), "menu" === n._element ? (e.setAttribute("aria-owns", a.id), a.setAttribute("role", "menu")) : a.setAttribute("role", "group"), a.menuItemsGroup = e, s.className = r, s.$ || (s.$ = Smart.Utilities.Extend(s)), s.container = a, s.menuItemsGroup = e, e.checkable && s.setAttribute("checkable", ""), s.setAttribute("check-mode", e.checkMode), s.setAttribute("role", "presentation"), a.itemContainer = s, a.contains(s) || a.appendChild(s), null !== e.dropDownHeight) {
                        let t = a.querySelector(".smart-spin-button.smart-scroll-button-near"),
                            o = a.querySelector(".smart-spin-button.smart-scroll-button-far");
                        t || (t = document.createElement("smart-repeat-button")), o || (o = document.createElement("smart-repeat-button")), t.className = "smart-menu-scroll-button smart-spin-button smart-scroll-button-near smart-hidden", t.setAttribute("aria-label", "Scroll up"), t.innerHTML = '<div class="smart-arrow smart-arrow-up" aria-hidden="true"></div>', t.animation = n.animation, t.unfocusable = !0, t.rightToLeft = n.rightToLeft, o.className = "smart-menu-scroll-button smart-spin-button smart-scroll-button-far smart-hidden", o.setAttribute("aria-label", "Scroll down"), o.innerHTML = '<div class="smart-arrow smart-arrow-down" aria-hidden="true"></div>', o.animation = n.animation, o.unfocusable = !0, o.rightToLeft = n.rightToLeft, a.contains(t) || a.insertBefore(t, s), a.contains(o) || a.appendChild(o), a.$.addClass("drop-down-height-set"), s.dropDownHeightSet = !0, s.checkOverflow = !0, a.style.height = e.dropDownHeight + "px", n._containersFixedHeight.push(a), n._additionalScrollButtons.push([t, o])
                    }
                    return a
                }
                _discardKeyboardHover(e) {
                    const t = this;
                    t._focusedViaKeyboard && (!e && t._focusedViaKeyboard instanceof Smart.MenuItemsGroup && t._isContainerOpened(t._focusedViaKeyboard.level + 1, t._focusedViaKeyboard.container) || (t._focusedViaKeyboard.$.removeClass("focus"), t._focusedViaKeyboard.removeAttribute("focus"), t._focusedViaKeyboard.$.removeClass("hover"), t._focusedViaKeyboard.removeAttribute("hover"), t._focusedViaKeyboard = void 0))
                }
                _documentDownHandler(e) { const t = this; "down" === t.closeAction && t._closeOnDocumentInteraction(e.originalEvent) }
                _documentUpHandler(e) {
                    const t = this,
                        n = e.originalEvent.target;
                    if (t.disabled || t.displayLoadingIndicator || !n.closest) return;
                    const o = "up" === t.closeAction && t._closeOnDocumentInteraction(e.originalEvent);
                    if (o) return;
                    let i, r;
                    if (t.isInShadowDOM ? (i = t.isInShadowDOM ? t.getRootNode().activeElement : t.shadowRoot && t.shadowRoot.activeElement || document.activeElement, r = t.$.container.contains(e.originalEvent.composedPath()[0])) : (i = document.activeElement, r = t.contains(n)), !o && t !== i && null === i.closest("[template-applied]")) {
                        if (r || n.closest(".smart-list-menu-view") === t.$.view) return void t.focus();
                        const e = n.closest(".smart-drop-down-repositioned");
                        e && e.ownerElement === t && t.focus()
                    }
                }
                _closeOnDocumentInteraction(e) {
                    const t = this,
                        n = e.target;
                    let o, i;
                    if (t.isInShadowDOM ? (o = e.composedPath()[0], i = t.$.container.contains(o)) : i = t.contains(n), "dropDown" === t.mode && t.opened) { const e = n.closest(".smart-drop-down-repositioned"); if (!(i || e && e.ownerElement === t)) return t.close({ trigger: "interaction", target: t.isInShadowDOM ? o : n }), !0 }
                    const r = (o || n).closest(".smart-input-drop-down-menu");
                    return (!r || !t.contains(r.ownerElement)) && (!i && null === n.closest(".smart-menu-drop-down") || o && o === t.$.mainContainer || n === t.$.mainContainer ? ("tree" === t.mode || t._close(), !0) : void 0)
                }
                _ensureVisible(e) {
                    const t = this;
                    if (t._minimized) return;
                    const n = t.mode,
                        o = t.$.mainContainer;
                    let i, r;
                    if ("tree" !== n && e.parentElement !== o) {
                        if (null === e.dropDownHeight) return;
                        i = e.parentElement, r = [i.container.children[0], i.container.children[2]]
                    } else i = o, r = [t.$.scrollButtonNear, t.$.scrollButtonFar];
                    if (i === o && (null === t.dropDownAppendTo && "tree" !== t.mode && !o.classList.contains("simple") || !i.$.hasClass("scroll-buttons-shown") && "hidden" !== t.overflow)) return;
                    const a = i.getBoundingClientRect(),
                        s = e.getBoundingClientRect();

                    function l(t, n, o) {
                        let r = e.firstElementChild[o] + t - i[o];
                        r < 0 && (r = t), i["scroll" + n] = r
                    }

                    function d(n, a) {
                        let s = e["offset" + n],
                            d = i[a];
                        "Top" !== n || i === o || r[0].$.hasClass("smart-hidden") || (s -= r[0][a]), l(s, n, a), t._updateScrollButtonVisibility(i, "Left" === n, r), d !== i[a] && l(s, n, a)
                    }
                    "tree" !== n ? (i === o && "horizontal" === n && (a.left > s.left || a.right < s.right) ? d("Left", "offsetWidth") : (a.top > s.top || a.bottom < s.bottom) && d("Top", "offsetHeight"), t._scrollInfo.set(i, { left: i.scrollLeft, top: i.scrollTop })) : t._ensureVisibleTreeMode(e, s, i, a, 0)
                }
                _ensureVisibleTreeMode(e, t, n, o, i) {
                    const r = this;
                    if (("menu" === r._element || "scrollButtons" === r.scrollMode) && !n.$.hasClass("scroll-buttons-shown") && "hidden" !== r.overflow) return;
                    const a = n.offsetHeight,
                        s = r.$scrollButtonNear.hasClass("smart-hidden");
                    let l;
                    if (o.top > t.top) l = r._getOffsetTop(e);
                    else {
                        let n = e.expanded ? e.firstElementChild.offsetHeight + parseInt(window.getComputedStyle(e.children[1]).marginTop, 10) : e.offsetHeight;
                        if ("tree" === r._element && (n += parseFloat(getComputedStyle(r).getPropertyValue("--smart-tree-item-vertical-offset")) || 0), !(o.bottom < t.top + n)) return;
                        l = r._getOffsetTop(e) - a + n + i
                    }
                    "tree" === r._element && "0" === e.path && (l -= parseFloat(getComputedStyle(r).getPropertyValue("--smart-tree-item-vertical-offset"))), n.scrollTop = l, "menu" !== r._element && "scrollButtons" !== r.scrollMode || r._updateScrollButtonVisibility(n, !1, [r.$.scrollButtonNear, r.$.scrollButtonFar]), "auto" === r.overflow && s && !r.$scrollButtonNear.hasClass("smart-hidden") && (n.scrollTop += a - n.offsetHeight), r._scrollInfo.set(n, { left: n.scrollLeft, top: n.scrollTop })
                }
                _escapeHandler(e, t, n) { e && (e.$.removeClass("focus"), e.removeAttribute("focus")), this._closeSubContainers(t, void 0, void 0, !0), this._hoverViaKeyboard(n.menuItemsGroup) }
                _expandItemsByDefault(e) {
                    const t = this;
                    if (0 === t._menuItemsGroupsToExpand.length && !e || "tree" !== t.mode && !t._minimized) return;
                    const n = t.hasAnimation,
                        o = t.animation;
                    n && (t.animation = "none"), e && t._collapseAll(!1);
                    for (let e = 0; e < t._menuItemsGroupsToExpand.length; e++) t.expandItem(t._menuItemsGroupsToExpand[e].path, void 0, !1);
                    n && (t.animation = o), t._menuItemsGroupsToExpand = []
                }
                _expandSection(e) {
                    const t = this,
                        n = e.style.height,
                        o = e.scrollHeight + "px";
                    e.style.height = o, t._treeAnimationInProgress = e, n !== o && (parseFloat(n) || parseFloat(o)) ? e.addEventListener("transitionend", t._transitionendHandlerExpand) : t._transitionendHandlerExpand(t, e)
                }
                _filterInputKeyupHandler() {
                    const e = this;
                    e._filterTimer && clearTimeout(e._filterTimer), e._filterTimer = setTimeout((function() {
                        const t = e.context;
                        e.context = e, e._applyFilter(e.$.filterInput.value, e._view), e._checkOverflow(), e.context = t
                    }), 300)
                }
                _findItem(e, t) {
                    if ("" === t) return e;
                    const n = e[this.filterMember || "label"];
                    if ("string" != typeof n) return null;
                    switch (this.filterMode) {
                        case "startsWith":
                            if (0 === n.indexOf(t)) return e;
                            break;
                        case "startsWithIgnoreCase":
                            if (0 === n.toLowerCase().indexOf(t.toLowerCase())) return e;
                            break;
                        case "doesNotContain":
                            if (n.indexOf(t) < 0) return e;
                            break;
                        case "doesNotContainIgnoreCase":
                            if (n.toLowerCase().indexOf(t.toLowerCase()) < 0) return e;
                            break;
                        case "contains":
                            if (n.indexOf(t) > -1) return e;
                            break;
                        case "containsIgnoreCase":
                            if (n.toLowerCase().indexOf(t.toLowerCase()) > -1) return e;
                            break;
                        case "equals":
                            if (0 === n.localeCompare(t)) return e;
                            break;
                        case "equalsIgnoreCase":
                            if (0 === n.toLowerCase().localeCompare(t.toLowerCase())) return e;
                            break;
                        case "endsWith":
                            if (n.endsWith(t)) return e;
                            break;
                        case "endsWithIgnoreCase":
                            if (n.toLowerCase().endsWith(t.toLowerCase())) return e
                    }
                    return null
                }
                _getFirstEnabledChild(e) {
                    const t = e.children;
                    for (let e = 0; e < t.length; e++)
                        if (this._isChildEnabled(t[e])) return t[e]
                }
                _getLastEnabledChild(e) {
                    const t = e.children;
                    for (let e = t.length - 1; e >= 0; e--)
                        if (this._isChildEnabled(t[e])) return t[e]
                }
                _getNextEnabledChild(e) {
                    if (e)
                        for (; e.nextElementSibling;) {
                            const t = e.nextElementSibling;
                            if (this._isChildEnabled(t)) return t;
                            e = t
                        }
                }
                _getOffsetTop(e) { let t = e.offsetTop; for (; e.offsetParent !== this.$.mainContainer;) t += (e = e.offsetParent).offsetTop; return t }
                _getPreviousEnabledChild(e) {
                    if (e)
                        for (; e.previousElementSibling;) {
                            const t = e.previousElementSibling;
                            if (this._isChildEnabled(t)) return t;
                            e = t
                        }
                }
                _hamburgerIconClickHandler(e, t) {
                    e && e.stopPropagation();
                    const n = this;
                    if (void 0 === t && (t = Smart.ListMenu && n instanceof Smart.ListMenu ? n.$.view : n.$.mainContainer), !n.disabled)
                        if (n._minimizedDropDownOpened) n._close();
                        else {
                            if (n._positionDetection.placeOverlay(), null !== n.dropDownAppendTo) {
                                const e = n.dropDownPosition,
                                    o = n.getBoundingClientRect(),
                                    i = n._positionDetection.getDropDownOffset(); - 1 !== e.indexOf("right") || "auto" === e ? n.rightToLeft ? (t.style.right = "initial", t.style.left = o.left + o.width - t.offsetWidth - i.x + "px") : (t.style.left = o.left + i.x + "px", t.style.right = "initial") : -1 !== e.indexOf("left") && (t.style.left = o.right - t.offsetWidth + i.x + "px", t.style.right = "initial"), -1 !== e.indexOf("bottom") || -1 !== e.indexOf("overlay") || "auto" === e ? t.style.top = o.bottom + i.y + "px" : -1 !== e.indexOf("top") && (t.style.top = o.top + i.y + "px")
                            } else t.style.right = "";
                            n._edgeMacFF && t.$.removeClass("not-in-view"), t.$.removeClass("smart-visibility-hidden"), n.$hamburgerIcon.addClass("smart-close-button"), n.$.hamburgerIcon.setAttribute("aria-expanded", !0), n._minimizedDropDownOpened = !0, n._browserBoundsDetection(t)
                        }
                }
                _handleOverflowChange() {
                    const e = this,
                        t = e.$.mainContainer;
                    if ((e._minimized || null === e.dropDownAppendTo && !t.classList.contains("simple") && "tree" !== e.mode) && !(Smart.ListMenu && e instanceof Smart.ListMenu)) return;
                    const n = e.overflow;
                    let o;
                    "horizontal" === e.mode ? (o = !0, t.scrollLeft = 0) : (o = !1, t.scrollTop = 0), "hidden" === n ? (t.classList.remove("scroll-buttons-shown"), e.$scrollButtonNear.addClass("smart-hidden"), e.$scrollButtonFar.addClass("smart-hidden")) : (e.$.scrollButtonNear.disabled = e.disabled, e.$.scrollButtonFar.disabled = e.disabled, "auto" === n ? (e.$scrollButtonNear.addClass("smart-hidden"), e.$scrollButtonFar.addClass("smart-hidden"), e._checkOverflow(t, o, [e.$.scrollButtonNear, e.$.scrollButtonFar])) : (t.classList.add("scroll-buttons-shown"), t.classList.remove("one-button-shown"), e.$scrollButtonNear.removeClass("smart-hidden"), e.$scrollButtonFar.removeClass("smart-hidden"), e._updateScrollButtonVisibility(t, o, [e.$.scrollButtonNear, e.$.scrollButtonFar]))), e._scrollInfo.set(t, { left: t.scrollLeft, top: t.scrollTop })
                }
                _hideMainContainerScrollButtons() {
                    const e = this;
                    e.$scrollButtonNear.addClass("smart-hidden"), e.$scrollButtonFar.addClass("smart-hidden"), e.$mainContainer.removeClass("scroll-buttons-shown"), e.$mainContainer.removeClass("one-button-shown")
                }
                _hoverViaKeyboard(e) { e && (e.$.addClass("focus"), e.setAttribute("focus", ""), this._focusedViaKeyboard = e, this._ensureVisible(e)) }
                _isBranchExpanded(e) { if ("tree" !== this.mode) return !0; let t = !0; for (; e.parentItem;) t = t && e.parentItem.expanded, e = e.parentItem; return t }
                _isChildEnabled(e) { return !(e.disabled || e.templateApplied || e.hidden || e instanceof HTMLDivElement || 0 === e.offsetHeight) }
                _isContainerOpened(e, t) { const n = this; return "tree" === n.mode || n._minimized ? (n._openedContainers[e] || (n._openedContainers[e] = []), -1 !== n._openedContainers[e].indexOf(t)) : n._openedContainers[e] === t }
                _keydownHandler(e) {
                    const t = this;
                    let n = e.key;
                    if (t.getRootNode().activeElement !== t || -1 === ["ArrowDown", "ArrowLeft", "ArrowRight", "ArrowUp", "End", "Enter", "Escape", "Home", " "].indexOf(n) || t.disabled) return;
                    e.preventDefault();
                    const o = t.mode;
                    if ("tree" === o || t._minimized) return void t._keydownHandlerTreeMode(n);
                    const i = t.dropDownPosition,
                        r = -1 !== i.indexOf("left"),
                        a = "top-left" === i || "top-right" === i,
                        s = t._openedContainers;
                    let l, d = t.$.mainContainer,
                        m = 1;
                    for (let e = s.length - 1; e >= 0; e--)
                        if (void 0 !== s[e]) { d = s[e], m = d.level, d = d.itemContainer; break }
                    switch (l = d.querySelector('[focus][level="' + m + '"]'), t.rightToLeft && ("ArrowLeft" === n ? n = "ArrowRight" : "ArrowRight" === n && (n = "ArrowLeft")), n) {
                        case "ArrowDown":
                            1 === m ? "horizontal" !== o || a ? "horizontal" !== o && t._levelOneNavigate("_getFirstEnabledChild", l, d) : t._levelOneOpenDropDown(l) : t._navigate("_getNextEnabledChild", l, d);
                            break;
                        case "ArrowLeft":
                            r ? 1 === m ? "horizontal" === o ? t._levelOneNavigate("_getLastEnabledChild", l, d) : t._levelOneOpenDropDown(l) : l instanceof Smart.MenuItemsGroup ? t._selectionHandler({ target: l, isTrusted: !0 }) : t._levelOneNavigateFromLowerLevel("_getPreviousEnabledChild", l) : t._arrowLeftHandler(m, o, l, d);
                            break;
                        case "ArrowRight":
                            r ? 1 === m ? "horizontal" === o && t._levelOneNavigate("_getFirstEnabledChild", l, d) : 2 === m ? t._levelOneNavigateFromLowerLevel("_getNextEnabledChild", l) : t._escapeHandler(l, m, d) : t._arrowRightHandler(m, o, l, d);
                            break;
                        case "ArrowUp":
                            1 === m ? "horizontal" === o && a ? t._levelOneOpenDropDown(l) : "horizontal" !== o && t._levelOneNavigate("_getLastEnabledChild", l, d) : t._navigate("_getPreviousEnabledChild", l, d);
                            break;
                        case "End":
                        case "Home":
                            { const e = "End" === n ? t._getLastEnabledChild(d) : t._getFirstEnabledChild(d); if (!e || l === e) return;l && (l.$.removeClass("focus"), l.removeAttribute("focus")), t._hoverViaKeyboard(e); break }
                        case "Enter":
                            l && t._selectionHandler({ target: l, isTrusted: !0 });
                            break;
                        case "Escape":
                            m > 1 ? (2 === m && t._positionDetection.removeOverlay(), t._escapeHandler(l, m, d)) : "dropDown" === o && t.opened && t.close({ trigger: "interaction", target: "Escape" });
                            break;
                        case " ":
                            l && t._toggleItem(l)
                    }
                }
                _keydownHandlerTreeMode(e) {
                    const t = this,
                        n = Array.from(t.$.mainContainer.querySelectorAll("smart-menu-item, smart-menu-items-group")),
                        o = t.$.mainContainer.getElementsByClassName("focus")[0];

                    function i(e) { const n = e.level; return !1 === e.disabled && !0 !== e.templateApplied && (1 === n || n > 1 && t._isContainerOpened(n, e.parentElement.container) && e.getBoundingClientRect().height > 0) }

                    function r(e) {
                        for (let r = e; r < n.length; r++) {
                            const e = n[r];
                            if (i(e)) {
                                if (o) {
                                    if (o === e) break;
                                    o.$.removeClass("focus"), o.removeAttribute("focus")
                                }
                                t._hoverViaKeyboard(e);
                                break
                            }
                        }
                    }

                    function a(e) {
                        for (let r = e; r >= 0; r--) {
                            const e = n[r];
                            if (i(e)) {
                                if (o) {
                                    if (o === e) break;
                                    o.$.removeClass("focus"), o.removeAttribute("focus")
                                }
                                t._hoverViaKeyboard(e);
                                break
                            }
                        }
                    }

                    function s() { o.level > 1 && (o.$.removeClass("focus"), o.removeAttribute("focus"), t._hoverViaKeyboard(o.parentItem)) }
                    let l;
                    switch (e) {
                        case "ArrowDown":
                            l = o ? n.indexOf(o) + 1 : 0, r(l);
                            break;
                        case "ArrowLeft":
                            if (!o) return;
                            if (o instanceof Smart.MenuItem) s();
                            else {
                                if (t._isContainerOpened(o.level + 1, o.container)) return void t._closeSubContainers(o.level + 1, o.container, !0, !0);
                                s()
                            }
                            break;
                        case "ArrowRight":
                            if (!o || o instanceof Smart.MenuItem) return;
                            t._isContainerOpened(o.level + 1, o.container) ? (o.$.removeClass("focus"), o.removeAttribute("focus"), t._hoverViaKeyboard(t._getFirstEnabledChild(o.itemContainer))) : t._selectionHandler({ target: o, type: "keydown", isTrusted: !0 }, o);
                            break;
                        case "ArrowUp":
                            l = o ? n.indexOf(o) - 1 : n.length - 1, a(l);
                            break;
                        case "End":
                            a(n.length - 1);
                            break;
                        case "Enter":
                            t._minimized && !t._minimizedDropDownOpened ? t._hamburgerIconClickHandler(void 0, t.$.mainContainer) : o && t._selectionHandler({ target: o, type: "keydown", isTrusted: !0 });
                            break;
                        case "Escape":
                            t._minimized && t._minimizedDropDownOpened && t._close();
                            break;
                        case "Home":
                            r(0);
                            break;
                        case " ":
                            o && t._toggleItem(o)
                    }
                }
                _lazyInitItems() {
                    const e = this;
                    e._inLazyInit || (e._inLazyInit = !0, e._menuItems = {}, e._processHTML(e.$.mainContainer, 1), e._expandItemsByDefault(), e._refreshCheckableItems(), cancelAnimationFrame(Smart.Menu.processTimer), delete Smart.Menu.processTimer, e._inLazyInit = !1, e.$.scrollViewer && e.$.scrollViewer.refresh())
                }
                _levelOneNavigate(e, t, n) {
                    const o = this;
                    if (t) "_getLastEnabledChild" === e ? o._navigate("_getPreviousEnabledChild", t, n) : o._navigate("_getNextEnabledChild", t, n);
                    else {
                        const t = o[e](n);
                        t && o._hoverViaKeyboard(t)
                    }
                }
                _levelOneNavigateFromLowerLevel(e, t) {
                    const n = this,
                        o = n[e](n._openedContainers[2].menuItemsGroup);
                    o && (t && (t.$.removeClass("focus"), t.removeAttribute("focus")), n._closeSubContainers(2), o instanceof Smart.MenuItemsGroup ? n._selectionHandler({ target: o, isTrusted: !0 }) : n._hoverViaKeyboard(o))
                }
                _levelOneOpenDropDown(e) { e && e instanceof Smart.MenuItemsGroup && this._selectionHandler({ target: e, isTrusted: !0 }) }
                _mainContainerHandler(e) {
                    const t = this;
                    if (t._minimized && null !== t.dropDownAppendTo) switch (e.type) {
                        case "click":
                            t._selectionHandler(e);
                            break;
                        case "mouseleave":
                            t._mouseleaveHandler(e);
                            break;
                        case "mouseout":
                        case "mouseover":
                            t._mouseoutMouseoverHandler(e)
                    }
                }
                _menuItemSelectionHandler(e, t) {
                    const n = this;

                    function o() { n.enableShadowDOM && (n.shadowRoot.activeElement || document.activeElement) !== n && null !== n.dropDownAppendTo && "click" === t.type && !n.shadowRoot.contains(e) ? n.focus() : document.activeElement === n || null === n.dropDownAppendTo || "click" !== t.type || n.contains(e) || n.focus() }
                    if (e.disabled || e.templateApplied) o();
                    else {
                        if (!n._toggleItem(e)) {
                            if (n.$.fireEvent("itemClick", { item: e, label: e.label, value: e.value }), t.target && "A" !== t.target.nodeName) {
                                const t = e.querySelector("a");
                                t && t.click()
                            }
                            if ("tree" !== n.mode && (n._close(), "dropDown" === n.mode)) return n._ripple(e, t), void n.close({ trigger: "interaction", target: e })
                        }
                        n._ripple(e, t), o()
                    }
                }
                _menuItemsGroupSelectionHandler(e, t, n) {
                    const o = this,
                        i = o.mode,
                        r = e.container,
                        a = r.level,
                        s = "tree" !== i && !o._minimized;
                    if (o._treeAnimationInProgress === r) return;
                    if (o._discardKeyboardHover(), o.getRootNode().activeElement === o || null === o.dropDownAppendTo || "click" !== t.type || o.contains(t.target) || o.focus(), "click" === t.type && (!t.target.classList.contains("smart-" + o._element + "-items-group-arrow") && o._toggleItem(e) || "mouseenter" === o.selectionMode && "tree" !== i && !o._minimized)) return;
                    let l = o.hasAnimation;
                    if (o._isContainerOpened(a, r)) o._closeSubContainers(a, r, !0, !1 !== n), s && e.hasAttribute("focus") && (o._focusedViaKeyboard = e);
                    else {
                        if (o.$.fireEvent("expanding", { item: e, label: e.label, path: e.path, value: e.value, children: e.itemContainer.children }).defaultPrevented) return;
                        if (o._positionDetection.placeOverlay(), s && o._closeSubContainers(a), l && !s && ("expand" !== t.type && (o._ensureVisibleOnTransitionend = e), o._expandSection(r)), o._edgeMacFF && 2 === a && s && r.$.removeClass("not-in-view"), r.$.removeClass("smart-visibility-hidden"), s || "expand" !== t.type) {
                            if (s) "keydown" === t.type && (o._focusedViaKeyboard = e);
                            else {
                                const t = o.$.mainContainer.getElementsByClassName("focus")[0];
                                t && (t.$.removeClass("focus"), t.removeAttribute("focus")), o._focusedViaKeyboard = e
                            }
                            e.$.addClass("focus"), e.setAttribute("focus", "")
                        }
                        if (e.$.addClass("smart-" + o._element + "-items-group-opened"), e.$.addClass("smart-" + o._element + "-items-group-expanded"), e.setAttribute("aria-expanded", !0), o._addOpenedContainer(a, r), s) {
                            if (o._ensureVisible(e), e.level > 1 && e.parentElement.dropDownHeightSet) {
                                const t = o.dropDownPosition,
                                    n = e.getBoundingClientRect().top - e.parentElement.container.getBoundingClientRect().top; - 1 !== t.indexOf("bottom") || "auto" === t ? r.style.top = n + "px" : -1 !== t.indexOf("top") ? r.style.top = n + e.offsetHeight + "px" : r.style.top = n + e.offsetHeight / 2 + "px"
                            }
                            r.itemContainer.checkOverflow && r.itemContainer.dropDownHeightSet && (o._checkOverflow(r.itemContainer, !1, [r.children[0], r.children[2]]), delete r.itemContainer.checkOverflow)
                        }
                        o._positionExternalContainer(r, e), "tree" === i || o._minimized ? l || o._browserBoundsDetection(o.$.mainContainer) : o._browserBoundsDetection(r), void 0 === t.type && o._hoverViaKeyboard(o._getFirstEnabledChild(e.itemContainer)), !1 !== n && o.$.fireEvent("expand", { item: e, label: e.label, path: e.path, value: e.value, children: e.itemContainer.children })
                    }
                    s ? o._ripple(e, t) : "tree" !== i || l || (o._checkOverflow(o.$.mainContainer, !1, [o.$.scrollButtonNear, o.$.scrollButtonFar]), o._minimized || "expand" === t.type || o._ensureVisible(e))
                }
                _mouseenterHandler() {
                    const e = this;
                    e.autoFocusOnMouseenter && e.getRootNode().activeElement !== e && e.focus()
                }
                _mouseleaveHandler(e) {
                    const t = this;
                    if ("mouseenter" === t.selectionMode && "tree" !== t.mode && !t._minimized) {
                        if (null !== t.dropDownAppendTo && e.relatedTarget)
                            if (t.contains(e.target)) { const n = e.relatedTarget.closest(".smart-menu-drop-down"); if (n && n.ownerElement === t) return } else if (t.contains(e.relatedTarget)) return;
                        t._isElementHovered = !1, t._autoCloseTimeout = setTimeout((function() {
                            const e = t.context;
                            clearTimeout(t._autoCloseTimeout), t._isElementHovered || (t.context = t, t._close(), t.context = e)
                        }), t.autoCloseDelay)
                    }
                }
                _mouseoutMouseoverHandler(e) {
                    const t = this;
                    if (t.disabled || t.displayLoadingIndicator) return;
                    let n = e.target.closest("smart-menu-item") || e.target.closest("smart-menu-items-group");
                    if (t.enableShadowDOM && (n = e.composedPath()[0].closest("smart-menu-item") || e.composedPath()[0].closest("smart-menu-items-group") || n), "mouseover" === e.type && (t._isElementHovered = !0), null !== n && !n.disabled && !n.templateApplied && ("tree" !== t.mode && !t._minimized || !n.hasAttribute("focus") || !e.relatedTarget || e.target.parentElement !== e.relatedTarget && e.relatedTarget.parentElement !== e.target))
                        if (t._discardKeyboardHover(!1), "mouseover" === e.type) {
                            "mouseenter" !== t.selectionMode || "tree" === t.mode || t._minimized || (n instanceof Smart.MenuItemsGroup && !n.hasAttribute("hover") ? t._selectionHandler(e, n) : n instanceof Smart.MenuItem && t._closeSubContainers(n.level + 1));
                            const o = e.target.closest(".smart-menu-drop-down");
                            (!o || o && !n.contains(o)) && (n.$.addClass("hover"), n.setAttribute("hover", ""), t._discardKeyboardHover(!0))
                        } else {
                            if ("tree" !== t.mode && !t._minimized && ("mouseenter" === t.selectionMode && e.relatedTarget === t.$.mainContainer && t._close(), n instanceof Smart.MenuItemsGroup && n.container && !n.container.$.hasClass("smart-visibility-hidden"))) return;
                            n.$.removeClass("hover"), n.removeAttribute("hover")
                        }
                }
                _moveDropDownsToExternalContainer() {
                    const e = this;
                    for (let t = 0; t < e._containersInBody.length; t++) {
                        const n = e._containersInBody[t];
                        e._dropDownParent.appendChild(n), n.$.listen("click", e._selectionHandler.bind(e)), n.$.listen("mouseleave", e._mouseleaveHandler.bind(e)), n.$.listen("mouseout", e._mouseoutMouseoverHandler.bind(e)), n.$.listen("mouseover", e._mouseoutMouseoverHandler.bind(e))
                    }
                    for (let t = 0; t < e._containers.length; t++) {
                        const n = e._containers[t];
                        n.ownerElement = e, "" !== e.theme && n.classList.add(e.theme), e.rightToLeft && n.setAttribute("right-to-left", ""), n.classList.add("smart-drop-down-repositioned"), n.setAttribute("mode", e.mode), n.setAttribute("drop-down-position", e.dropDownPosition), e.checkboxes && n.setAttribute("checkboxes", "")
                    }
                }
                _moveDropDownsToMenu() {
                    const e = this;
                    for (let t = 0; t < e._containersInBody.length; t++) {
                        const n = e._containersInBody[t];
                        n.$.unlisten("click"), n.$.unlisten("mouseleave"), n.$.unlisten("mouseout"), n.$.unlisten("mouseover"), n.style.left = "", n.style.right = "", n.style.top = "", n.style.marginLeft = "", n.style.marginTop = "", n.menuItemsGroup.appendChild(n)
                    }
                    for (let t = 0; t < e._containers.length; t++) { const n = e._containers[t]; "" !== e.theme && n.classList.remove(e.theme), n.classList.remove("smart-drop-down-repositioned"), n.removeAttribute("mode"), n.removeAttribute("drop-down-position"), n.removeAttribute("checkboxes"), n.removeAttribute("right-to-left") }
                }
                _navigate(e, t, n) {
                    const o = this;
                    if (!t) return void("_getNextEnabledChild" === e ? o._hoverViaKeyboard(o._getFirstEnabledChild(n)) : o._hoverViaKeyboard(o._getLastEnabledChild(n)));
                    const i = o[e](t);
                    i && (t.$.removeClass("focus"), t.removeAttribute("focus"), o._hoverViaKeyboard(i))
                }
                _positionExternalContainer(e, t) {
                    const n = this;
                    if (null === n.dropDownAppendTo || 2 !== e.level) return;
                    const o = n.dropDownPosition,
                        i = n.mode,
                        r = t.getBoundingClientRect(),
                        a = n._positionDetection.getDropDownOffset(),
                        s = r.top + a.y,
                        l = r.bottom + a.y;
                    let d = r.left + a.x,
                        m = r.right + a.x;
                    switch (e.style.top = e.style.left = e.style.right = "", n.rightToLeft && (e.style.right = "initial"), -1 !== o.indexOf("left") ? (d -= e.offsetWidth, "horizontal" !== i && "overlay-left" !== o || (d += r.width), e.style.left = d + "px", e.style.right = "initial") : "horizontal" === i || "overlay-right" === o ? e.style.left = d + "px" : n.rightToLeft ? e.style.left = m - e.offsetWidth + "px" : e.style.left = d + r.width + "px", o) {
                        case "bottom-right":
                        case "bottom-left":
                        case "auto":
                            e.style.top = "horizontal" === i ? l + "px" : s + "px";
                            break;
                        case "top-right":
                        case "top-left":
                            e.style.top = "horizontal" === i ? s - e.offsetHeight + "px" : l - e.offsetHeight + "px";
                            break;
                        case "overlay-right":
                        case "overlay-left":
                            e.style.top = s + r.height / 2 + "px"
                    }
                }
                _processDataSource() {
                    const e = this,
                        t = e.dataSource,
                        n = e.displayMember,
                        o = e.itemsMember,
                        i = e.valueMember,
                        r = e.$.mainContainer,
                        a = document.createDocumentFragment();

                    function s(t, r) {
                        let a;
                        if (Array.isArray(t[o]) && t[o].length > 0) { a = document.createElement("smart-" + e._element + "-items-group"), !0 === t.checkable && a.set("checkable", !0), "string" == typeof t.checkMode && a.set("checkMode", t.checkMode), t.dropDownHeight && a.set("dropDownHeight", t.dropDownHeight), !0 === t.expanded && "tree" === e.mode && (a.set("expanded", !0), a.setAttribute("aria-expanded", !0)); for (let e = 0; e < t[o].length; e++) s(t[o][e], a) } else a = document.createElement("smart-" + e._element + "-item"), void 0 !== t.shortcut && a.set("shortcut", t.shortcut), t.customAttribute && a.setAttribute(t.customAttribute, "");
                        a.isDirty = !1, void 0 !== t.id && /^[A-Za-z]+[\w\-\:\.]*$/.test(t.id) && (a.id = t.id), !0 === t.checked && (a.set("checked", !0), a.setAttribute("aria-checked", !0)), !0 === t.disabled && a.set("disabled", !0), void 0 !== t[n] ? a.set("label", t[n]) : "string" == typeof t[o] && a.set("label", t[o]), !0 === t.selected && a.set("selected", !0), !0 === t.separator && a.set("separator", !0), void 0 !== t[i] && a.set("value", t[i]), r.appendChild(a)
                    }
                    r.innerHTML = "", r instanceof Smart.ScrollViewer && r.removeAll();
                    for (let e = 0; e < t.length; e++) s(t[e], a);
                    e.$.mainContainer.appendChild(a), e._processHTML(e.$.mainContainer, 1)
                }
                _processHTML(e, t, n) {
                    const o = this;
                    let i, r;
                    t > 1 && (i = o._createMenuItemsGroupContainer(e, t), r = i.itemContainer, (e.expanded || e.hasAttribute("expanded")) && "tree" === o.mode ? o._menuItemsGroupsToExpand.push(e) : (e.set("expanded", !1), e.removeAttribute("expanded"), e.setAttribute("aria-expanded", !1)));
                    const a = Array.from(e.children),
                        s = [],
                        l = document.createDocumentFragment();
                    let d = 0;
                    for (let n = 0; n < a.length; n++) {
                        if (t > 1 && 0 === n) { d++; continue }
                        const i = a[n];
                        i instanceof Smart.MenuItem || i instanceof Smart.MenuItemsGroup ? (o._createItemHTMLStructure(i, t, e, n - d), (i.checked || i.hasAttribute("checked")) && (i.disabled || i.hasAttribute("disabled") || i.templateApplied ? (i.set("checked", !1), i.removeAttribute("checked"), i.removeAttribute("aria-checked")) : s.push(i)), t > 1 && l.appendChild(i), i instanceof Smart.MenuItemsGroup && o._processHTML(i, t + 1)) : (i.parentElement.removeChild(i), d++)
                    }
                    if (t > 1) {
                        if (r.appendChild(l), e.container = i, e.itemContainer = r, e instanceof Smart.MenuItemsGroup) {
                            const n = document.createElement("div");
                            n.className = "smart-" + o._element + "-items-group-arrow", "menu" === o._element ? n.setAttribute("role", "presentation") : (n.setAttribute("role", "button"), n.setAttribute("aria-label", "Toggle")), o._setArrowDirection(n, t), e.firstElementChild.appendChild(n)
                        }
                        o._containers.push(i), 2 === t && (o._containersInBody.push(i), o._edgeMacFF && i.addEventListener("transitionend", (function(e) { e.target === this && this.$.hasClass("smart-visibility-hidden") && (this.style.left = "", this.style.top = "", this.$.addClass("not-in-view")) }))), null === o.dropDownAppendTo || "tree" === o.mode || o._minimized ? e.appendChild(i) : (i.ownerElement = o, o.rightToLeft ? i.setAttribute("right-to-left", "") : i.removeAttribute("right-to-left"), i.classList.add("smart-drop-down-repositioned"), i.setAttribute("mode", o.mode), i.setAttribute("drop-down-position", o.dropDownPosition), o.checkboxes && i.setAttribute("checkboxes", ""), "" !== o.theme && i.$.addClass(o.theme), i.setAttribute("animation", o.animation), 2 === t ? (o._dropDownParent.appendChild(i), i.$.listen("click", o._selectionHandler.bind(o)), i.$.listen("mouseleave", o._mouseleaveHandler.bind(o)), i.$.listen("mouseout", o._mouseoutMouseoverHandler.bind(o)), i.$.listen("mouseover", o._mouseoutMouseoverHandler.bind(o))) : e.appendChild(i))
                    }
                    o._validateRadioButtonSelection(e, t, s), o._sortItems && !1 !== n && o._sortItems(e)
                }
                _processUList() {
                    const e = this,
                        t = new RegExp(/<li>(.(?!<\/li>)|\n)*?<ul>/),
                        n = new RegExp(/<\/ul>(.|\n)*?<\/li>/);
                    let o = e.$.mainContainer.firstElementChild.innerHTML;
                    for (o = o.replace(/\r?\n|\r/g, ""), o = o.replace(/<li(.|\n)*?>/g, "<li>"), o = o.replace(/<li><\/li>/g, "<li> </li>"), o = o.replace(/<ul(.|\n)*?>/g, "<ul>"); t.test(o);) {
                        const n = t.exec(o),
                            i = "<smart-" + e._element + "-items-group>" + n[0].slice(4, n[0].length - 4);
                        o = o.replace(n[0], i)
                    }
                    for (; n.test(o);) {
                        const t = n.exec(o),
                            i = "</smart-" + e._element + "-items-group>";
                        o = o.replace(t[0], i)
                    }
                    o = o.replace(/li>/g, "smart-" + e._element + "-item>"), e.$.mainContainer.innerHTML = o
                }
                _refreshContainersArrays() {
                    const e = this;
                    for (let t = e._containers.length - 1; t >= 0; t--) {
                        const n = e._containers[t];
                        if (!document.body.contains(n)) {
                            e._containers.splice(t, 1);
                            const o = e._containersFixedHeight.indexOf(n);
                            o > -1 && (e._containersFixedHeight.splice(o, 1), e._additionalScrollButtons.splice(o, 1))
                        }
                    }
                    e._checkContainersLength()
                }
                _refreshItemPaths(e, t, n, o) {
                    const i = this;
                    let r;
                    r = t ? e : e.container.itemContainer;
                    const a = n ? n(e) : r.children;
                    for (let r = 0; r < a.length; r++) {
                        const s = a[r];
                        let l;
                        o && (s.originalIndex = r), l = t ? "" + r : e.path + "." + r, s.path = l, i._menuItems[l] = s, s instanceof Smart.MenuItemsGroup && i._refreshItemPaths(s, void 0, n, o)
                    }
                }
                _removeContainerFixedHeight() {
                    const e = this;
                    for (let t = 0; t < e._containersFixedHeight.length; t++) {
                        const n = e._containersFixedHeight[t];
                        n.style.height = "", n.itemContainer.$.removeClass("scroll-buttons-shown"), n.itemContainer.$.removeClass("one-button-shown"), n.children[0].$.addClass("smart-hidden"), n.children[2].$.addClass("smart-hidden"), n.itemContainer.checkOverflow = !0
                    }
                }
                _removeContainersInBody() {
                    const e = this;
                    if (null !== e.dropDownAppendTo && !e._minimized)
                        for (let t = 0; t < e._containersInBody.length; t++) e._containersInBody[t].remove()
                }
                _reparentMenu(e, t) {
                    const n = this;
                    if ("dropDown" === n.mode && (null !== n._dropDownParent || e) && n._dropDownParent !== n.parentElement) {
                        if (e && null !== t) { if (null === n._dropDownParent) return n._positionRelativeTo.appendChild(n), void(n._positionRelativeTo = null) } else n._positionRelativeTo = n.parentElement;
                        n._dropDownParent.appendChild(n)
                    }
                }
                refresh() {
                    const e = this;
                    if (e._suppressResizeHandler) return void delete e._suppressResizeHandler;
                    const t = e.minimizeWidth,
                        n = e.mode;
                    if (null !== t && "dropDown" !== n) {
                        if (e.offsetWidth <= t && !e._minimized) return void e.minimize();
                        e.offsetWidth > t && e.maximize()
                    }(null !== e.dropDownAppendTo || "tree" === n || e.$mainContainer.hasClass("simple")) && e._checkOverflow(e.$.mainContainer, "horizontal" === n, [e.$.scrollButtonNear, e.$.scrollButtonFar])
                }
                _resizeHandler() { this.refresh() }
                _ripple(e, t) { if (this.hasRippleAnimation && "click" === t.type) return Smart.Utilities.Animation.Ripple.animate(e, t.pageX, t.pageY), !0 }
                _scroll(e) {
                    if (e.closest("[template-applied]")) return;
                    const t = this,
                        n = t.$.mainContainer,
                        o = t.mode,
                        i = e.classList.contains("smart-scroll-button-near") ? -1 : 1;
                    let r;
                    if (e.parentElement === t.$.container) r = n, "tree" !== o && t._closeSubContainers(2), "horizontal" === t.mode ? (n.scrollLeft = n.scrollLeft + 10 * i, t._updateScrollButtonVisibility(n, !0, [t.$.scrollButtonNear, t.$.scrollButtonFar])) : (n.scrollTop = n.scrollTop + 10 * i, t._updateScrollButtonVisibility(n, !1, [t.$.scrollButtonNear, t.$.scrollButtonFar]));
                    else {
                        const n = e.parentElement,
                            o = n.itemContainer;
                        r = o, t._closeSubContainers(n.level + 1), o.scrollTop = o.scrollTop + 10 * i, t._updateScrollButtonVisibility(o, !1, [n.children[0], n.children[2]])
                    }
                    t._scrollInfo.set(r, { left: r.scrollLeft, top: r.scrollTop })
                }
                _selectionHandler(e, t) {
                    const n = this,
                        o = e.target;
                    if (o.closest("[template-applied]") && e.stopPropagation(), !n.disabled && !n.displayLoadingIndicator) {
                        if (void 0 === t) { if ("click" === e.type) { const t = o.closest("smart-repeat-button"); if (t) return void n._scroll(t, e) } if (!e.isTrusted) return; const i = o.closest("smart-" + n._element + "-item"); if (i) return void n._menuItemSelectionHandler(i, e); if ((t = o.closest("smart-" + n._element + "-items-group")) && (o === t.container || o === t.container.firstElementChild)) return }
                        t && !t.disabled && n._menuItemsGroupSelectionHandler(t, e)
                    }
                }
                _setArrowDirection(e, t) {
                    const n = this,
                        o = n.mode;
                    "tree" === o || n._minimized ? e.className = "smart-" + n._element + "-items-group-arrow down smart-arrow-down" : "overlay" !== n.dropDownPosition.slice(0, 7) ? 2 === t && "horizontal" === o ? "top" !== n.dropDownPosition.slice(0, 3) ? e.className = "smart-menu-items-group-arrow down smart-arrow-down" : e.className = "smart-menu-items-group-arrow up smart-arrow-up" : e.className = "smart-menu-items-group-arrow " + (n.rightToLeft ? "left smart-arrow-left" : "right smart-arrow-right") : e.className = "smart-menu-items-group-arrow minus"
                }
                _setFocusable() {
                    const e = this;
                    if (e.disabled || e.unfocusable) return void e.removeAttribute("tabindex");
                    const t = e.getAttribute("tabindex");
                    (null === t || t < 0) && e.setAttribute("tabindex", 0)
                }
                _setItemLabel(e, t) {
                    const n = this,
                        o = n.context,
                        i = e.querySelector(".smart-menu-item-label-element>span");
                    n.context = n, n._setLabel(t, i, e, !0), n._checkOverflow(n.$.mainContainer, "horizontal" === n.mode, [n.$.scrollButtonNear, n.$.scrollButtonFar]), n.context = o
                }
                _setLabel(e, t, n, o) {
                    const i = document.getElementById(e);
                    if (null !== i && "template" === i.tagName.toLowerCase()) {
                        const r = document.importNode(i.content, !0);
                        if (n instanceof Smart.MenuItem) t.appendChild(r), o && (n.setAttribute("template-applied", ""), n.templateApplied = !0);
                        else if (Smart.ListMenu && this instanceof Smart.ListMenu) {
                            const e = new RegExp(/{{title="(.*)"}}/);
                            for (let t = 0; t < r.childNodes.length; t++) e.test(r.childNodes[t].innerHTML) ? (n.titleLabel = e.exec(r.childNodes[t].innerHTML)[1], r.childNodes[t].innerHTML = r.childNodes[t].innerHTML.replace(e, "")) : e.test(r.childNodes[t].textContent) && (n.titleLabel = e.exec(r.childNodes[t].textContent)[1], r.childNodes[t].textContent = r.childNodes[t].textContent.replace(e, ""));
                            void 0 === n.titleLabel && (n.titleLabel = r.textContent), t.appendChild(r)
                        } else t.innerHTML = e, n.titleLabel = e
                    } else t.innerHTML = e, n instanceof Smart.MenuItemsGroup && (n.titleLabel = e)
                }
                _toggleItem(e) { const t = this; if (t.checkboxes) { const n = 1 === e.level ? t : e.parentItem; if (n.checkable) { const o = t._getItemCheckableInfo(e, n); let i = !1; return "none" !== o.checkMode && ("checkbox" === o.checkMode ? (i = !0, e.set("checked", !e.checked), e.checked ? e.setAttribute("aria-checked", !0) : e.removeAttribute("aria-checked"), t.$.fireEvent("itemCheckChange", { item: e, label: e.label, value: e.value, checked: e.checked })) : "radioButton" !== o.checkMode || e.checked || (i = !0, e.set("checked", !0), e.setAttribute("aria-checked", !0), t._uncheckSiblings(e, o.siblings), t.$.fireEvent("itemCheckChange", { item: e, label: e.label, value: e.value, checked: !0 })), e instanceof Smart.MenuItem && i && t.$.fireEvent("itemClick", { item: e, label: e.label, value: e.value }), "tree" === t.mode || "ListMenu" === t.elementName || t.preventCloseOnCheck || (t._close(), t.close()), !0) } } return !1 }
                _getItemCheckableInfo(e, t) {
                    const n = Array.from(e.parentElement.children),
                        o = t.checkMode.replace(/\s/g, "").split(",");
                    let i, r;
                    if (1 === o.length) i = o[0], r = n;
                    else {
                        let t = 0,
                            a = !1;
                        r = [];
                        for (let o = 0; o < n.length; o++) {
                            const i = n[o];
                            if (r.push(i), i === e && (a = !0), i.separator) {
                                if (!0 === a) break;
                                t++, r = []
                            }
                        }
                        i = o[t]
                    }
                    return { checkMode: i, siblings: r }
                }
                _refreshCheckableItems(e) {
                    const t = this,
                        n = !t.checkboxes;
                    (e ? [e] : [t].concat(t._containers.map((e => e.menuItemsGroup)))).forEach((e => {
                        const o = Array.from((e === t ? t.$.mainContainer : e.itemContainer).children);
                        let i = e.checkMode.replace(/\s/g, "").split(",");
                        if (n || !e.checkable || 1 === i.length) return void o.forEach((e => e.removeAttribute("check-type")));
                        let r = 0;
                        i = i.map((e => -1 === ["checkbox", "radioButton", "none"].indexOf(e) ? "none" : e));
                        let a = [],
                            s = [];
                        for (let e = 0; e < o.length; e++) {
                            const n = o[e];
                            let l = i[r];
                            if (void 0 === l && (l = i[r] = "none"), "none" !== l && t._isChildEnabled(n) || (n.checked = !1, n.removeAttribute("aria-checked")), "none" === l ? n.setAttribute("role", "menuitem") : "checkbox" === l ? n.setAttribute("role", "menuitemcheckbox") : "radioButton" === l && (n.setAttribute("role", "menuitemradio"), a.push(n), n.checked && s.push(n)), n.setAttribute("check-type", l), n.separator) {
                                if (a.length > 0)
                                    if (s.length > 1)
                                        for (let e = 0; e < s.length - 1; e++) s[e].checked = !1;
                                    else if (0 === s.length)
                                    for (let e = 0; e < a.length; e++)
                                        if (t._isChildEnabled(a[e])) { a[e].checked = !0; break }
                                a = [], s = [], r++
                            }
                        }
                        e.checkMode = i.join(", ")
                    }))
                }
                _transitionendHandler(e) { const t = this; "dropDown" === t.mode && t.opened && e.target === t && "opacity" === e.propertyName && (t._checkOverflowOnOpen && (t._checkOverflow(t.$.mainContainer, !1, [t.$.scrollButtonNear, t.$.scrollButtonFar]), delete t._checkOverflowOnOpen), t.getRootNode().activeElement === t || t._noAutoFocus || t.focus()) }
                _transitionendHandlerCollapse() {
                    let e, t;
                    if (1 === arguments.length) {
                        if ("visibility" === arguments[0].propertyName) return;
                        t = this, e = t.menuItemsGroup.menu
                    } else e = arguments[0], t = arguments[1];
                    t.menuItemsGroup.$.removeClass("smart-" + e._element + "-items-group-expanded"), t.menuItemsGroup.setAttribute("aria-expanded", !1), t.removeEventListener("transitionend", e._transitionendHandlerCollapse), t.style.height = null, t.$.addClass("smart-visibility-hidden"), e._checkOverflow(e.$.mainContainer, !1, [e.$.scrollButtonNear, e.$.scrollButtonFar]), e._minimized && e._browserBoundsDetection(e.$.mainContainer), delete e._treeAnimationInProgress
                }
                _transitionendHandlerExpand() {
                    let e, t;
                    if (1 === arguments.length) {
                        if ("visibility" === arguments[0].propertyName) return;
                        t = this, e = t.menuItemsGroup.menu
                    } else e = arguments[0], t = arguments[1];
                    t.removeEventListener("transitionend", e._transitionendHandlerExpand), t.style.height = null, e._checkOverflow(e.$.mainContainer, !1, [e.$.scrollButtonNear, e.$.scrollButtonFar]), e._minimized && e._browserBoundsDetection(e.$.mainContainer), e._ensureVisibleOnTransitionend && (e._ensureVisible(e._ensureVisibleOnTransitionend), delete e._ensureVisibleOnTransitionend), delete e._treeAnimationInProgress
                }
                _uncheckSiblings(e, t) {
                    for (let n = 0; n < t.length; n++) {
                        const o = t[n];
                        o !== e && o.checked && (o.set("checked", !1), o.removeAttribute("aria-checked"), this.$.fireEvent("itemCheckChange", { item: o, label: o.label, value: o.value, checked: !1 }))
                    }
                }
                _unsortItems(e, t) {
                    const n = this;
                    let o, i, r = [];
                    e === n.$.mainContainer ? (i = e, o = e.children) : (i = e.container.firstElementChild, o = i.children);
                    for (let e = 0; e < o.length; e++) {
                        const i = o[e];
                        r[i.originalIndex] = i, i instanceof Smart.MenuItemsGroup && void 0 === t && n._unsortItems(i)
                    }
                    if (!(r.length < 2))
                        for (let e = 0; e < r.length; e++) i.appendChild(r[e])
                }
                _updateItemRoles(e) {
                    const t = this;
                    for (let n in t._menuItems) {
                        const o = t._menuItems[n],
                            i = o.parentItem || t;
                        e && i !== e || (t.checkboxes && i.checkable ? o.setAttribute("role", "checkbox" === i.checkMode ? "menuitemcheckbox" : "menuitemradio") : o.setAttribute("role", "menuitem"))
                    }
                    t._refreshCheckableItems(e)
                }
                _updateScrollButtonVisibility(e, t, n) {
                    const o = this,
                        i = o.overflow,
                        r = e === o.$.mainContainer;
                    if (r && "hidden" === i) return;
                    let a, s, l, d = !0,
                        m = !0;
                    if (t ? (a = "scrollLeft", s = "offsetWidth", l = "scrollWidth") : (a = "scrollTop", s = "offsetHeight", l = "scrollHeight"), 0 === Math.round(e[a]) && (d = !1), Math.round(e[s] + e[a]) >= Math.round(e[l]) && (m = !1), r && "auto" !== i) "scroll" !== i || o.disabled || (n[0].disabled = !d, n[1].disabled = !m);
                    else {
                        if (d && m) return n[0].$.removeClass("smart-hidden"), n[1].$.removeClass("smart-hidden"), void e.classList.remove("one-button-shown");
                        d ? n[0].$.removeClass("smart-hidden") : n[0].$.addClass("smart-hidden"), m ? n[1].$.removeClass("smart-hidden") : n[1].$.addClass("smart-hidden"), e.classList.add("one-button-shown")
                    }
                }
                _validateRadioButtonSelection(e, t, n) {
                    const o = this;
                    if (o.checkboxes) {
                        let i, r;
                        if (1 === t ? (i = o, r = o.$.mainContainer) : (i = e, r = e.itemContainer), "radioButton" === i.checkMode && i.checkable)
                            if (n.length > 1)
                                for (let e = n.length - 2; e >= 0; e--) n[e].set("checked", !1), n[e].removeAttribute("aria-checked");
                            else if (0 === n.length) {
                            const e = o._getFirstEnabledChild(r);
                            e && (e.set("checked", !0), e.setAttribute("aria-checked", !0))
                        }
                    }
                }
            });

            /***/
        }),

        /***/
        8649:
        /***/
            (() => {

            Smart("smart-radio-button", class extends Smart.ToggleButton {
                static get properties() { return { checkMode: { value: "both", allowedValues: ["both", "input", "label"], type: "string" }, type: { value: "radio", type: "string", defaultReflectToAttribute: !0, readonly: !0 }, groupName: { value: "", type: "string" } } }
                template() { return "<div  id='container' class='smart-container'>\n                 <div class ='smart-overlay'></div>\n                 <span id='radioButtonInput' class ='smart-input'></span>\n                 <span id='radioButtonLabel' inner-h-t-m-l='[[innerHTML]]' class ='smart-label'><content></content></span>\n                 <input id='hiddenInput' class ='smart-hidden-input' type='hidden'>\n               </div>" }
                static get listeners() { return { down: "_downHandler", "document.up": "_documentUpHandler", mouseenter: "_elementMouseEnterHandler", "radioButtonInput.mouseenter": "_radioMouseEnterHandler", "radioButtonInput.mouseleave": "_radioMouseLeaveHandler", focus: "_focusHandler", blur: "_blurHandler" } }
                static get styleUrls() { return ["smart.toggle.css"] }
                _radioMouseEnterHandler() { this.$.setAttributeValue("hover", !0) }
                _radioMouseLeaveHandler() { this.$.setAttributeValue("hover", !1) }
                _focusHandler() { this.$.setAttributeValue("focus", !0) }
                _blurHandler() { this.$.setAttributeValue("focus", !1) }
                _mouseEnterHandler() { this.$.setAttributeValue("hover", !0) }
                _mouseLeaveHandler() { this.$.setAttributeValue("hover", !1) }
                ready() {
                    const e = this;
                    super.ready(), e.classList.add("smart-toggle-box"), e._handleMultipleCheckedInstances(), e._updateHidenInputNameAndValue()
                }
                _downHandler(e) {
                    const t = this,
                        n = t.enableShadowDOM ? e.originalEvent.composedPath()[0] : e.originalEvent.target;
                    if (!(t.disabled || t.readonly || "input" === t.checkMode && n !== t.$.radioButtonInput || "label" === t.checkMode && n !== t.$.radioButtonLabel)) {
                        if (t.$.setAttributeValue("active", !0), t.hasRippleAnimation) {
                            const e = t.$.radioButtonInput.getBoundingClientRect(),
                                n = window.scrollX || window.pageXOffset,
                                a = window.scrollY || window.pageYOffset;
                            Smart.Utilities.Animation.Ripple.animate(t.$.radioButtonInput, e.left + e.width / 2 + n, e.top + e.height / 2 + a)
                        }
                        t._preventAction ? t._preventAction = !1 : ("release" !== t.clickMode && "pressAndRelease" !== t.clickMode || (t._pressed = !0), "press" !== t.clickMode && "pressAndRelease" !== t.clickMode || ("pressAndRelease" === t.clickMode && ("" === t.groupName ? t._checkedBeforeChange = t.parentNode.querySelector("smart-radio-button[checked]") : t._checkedBeforeChange = document.querySelector('smart-radio-button[group-name="' + t.groupName + '"][checked]')), t._handleMouseInteraction()))
                    }
                }
                _elementMouseEnterHandler() { const e = this; "hover" !== e.clickMode || e.disabled || e.readonly || e._handleMouseInteraction() }
                _documentUpHandler(e) {
                    const t = this,
                        n = t.enableShadowDOM ? e.originalEvent.composedPath()[0] : e.originalEvent.target;
                    !t._pressed || t.disabled || t.readonly || "input" === t.checkMode && n !== t.$.radioButtonInput || "label" === t.checkMode && n !== t.$.radioButtonLabel || "pointercancel" === e.originalEvent.type || ("release" === t.clickMode ? t._handleMouseInteraction() : (null === t._checkedBeforeChange ? (t.$.fireEvent("change", { value: !1, oldValue: !0, changeType: "pointer" }), t.$.fireEvent("uncheckValue", { changeType: "pointer" }), t.checked = !1) : t._checkedBeforeChange._changeCheckState("pointer"), t.focus(), t._updateHidenInputNameAndValue()), t.$.setAttributeValue("active", !1), t._pressed = !1)
                }
                _handleMouseInteraction() {
                    const e = this;
                    e._handleTextSelection(), e._changeCheckState("pointer"), e.focus(), e._updateHidenInputNameAndValue()
                }
                _handleMultipleCheckedInstances() {
                    const e = Array.from(document.querySelectorAll('smart-radio-button[group-name="' + this.groupName + '"][checked]')),
                        t = Array.from(document.querySelectorAll('smart-ui-radio-button[group-name="' + this.groupName + '"][checked]')),
                        n = e.length + t.length;
                    n < 2 || e.concat(...t).forEach(((e, t) => t < n - 1 && (e.checked = !1)))
                }
                _changeCheckState(e) {
                    const t = this;
                    let n = document.querySelectorAll('smart-radio-button[group-name="' + t.groupName + '"]'),
                        a = document.querySelectorAll('smart-ui-radio-button[group-name="' + t.groupName + '"]'),
                        o = Array.from(n).concat(...a);
                    if (!0 === t.checked && "api" === e || !1 === t.checked)
                        if (o.length > 0) t._changeCheckStateInGroup(o, e);
                        else {
                            let r = t.parentNode;
                            t.getRootNode().host ? (r = t.getRootNode().host.parentNode, n = r.querySelectorAll("smart-radio-button:not([group-name])"), a = r.querySelectorAll("smart-ui-radio-button:not([group-name])"), o = Array.from(n).concat(...a)) : o = r.querySelectorAll("smart-radio-button:not([group-name])"), t._changeCheckStateInGroup(o, e)
                        }
                }
                _changeCheckStateInGroup(e, t) {
                    const n = this,
                        a = n.getRootNode().host ? n.getRootNode().host : n;
                    for (let t = 0; t < e.length; t++) e[t]._isUpdating = !0, e[t] === a ? a.checked = !0 : e[t].checked && (e[t].checked = !1), e[t]._isUpdating = !1;
                    a.nativeElement ? (a.nativeElement.$.fireEvent("change", { value: !0, oldValue: !1, changeType: t }), a.nativeElement.$.fireEvent("checkValue", { changeType: t })) : (a.$.fireEvent("change", { value: !0, oldValue: !1, changeType: t }), a.$.fireEvent("checkValue", { changeType: t }))
                }
                propertyChangedHandler(e, t, n) {
                    const a = this;
                    switch (e) {
                        case "value":
                            a._updateHidenInputNameAndValue();
                            break;
                        case "checked":
                            a._isUpdating || a._changeCheckState("api"), a._updateHidenInputNameAndValue();
                            break;
                        case "name":
                            a._updateHidenInputName();
                            break;
                        default:
                            super.propertyChangedHandler(e, t, n)
                    }
                }
            });

            /***/
        }),

        /***/
        9135:
        /***/
            (() => {

            Smart("smart-scroll-bar", class extends Smart.BaseElement {
                static get properties() { return { clickRepeatDelay: { type: "integer", value: 50 }, largeStep: { type: "integer", value: 100 }, min: { type: "integer", value: 0 }, max: { type: "integer", value: 1e3 }, mechanicalAction: { value: "switchWhileDragging", allowedValues: ["switchUntilReleased", "switchWhenReleased", "switchWhileDragging"], type: "string" }, orientation: { type: "string", value: "horizontal", allowedValues: ["horizontal", "vertical"] }, step: { type: "integer", value: 10 }, showButtons: { type: "boolean", value: !0, defaultReflectToAttribute: !0 }, value: { type: "integer", value: 0 } } }
                static get styleUrls() { return ["smart.scrollbar.css"] }
                template() { return '<div id="container" class="smart-container" role="presentation">\n                    <div id="nearButton" class="smart-scroll-button smart-arrow-left" role="presentation" aria-hidden="true"></div>\n                    <div  id="track" class="smart-track" role="presentation">\n                        <div id="thumb" class="smart-thumb" role="presentation"></div>\n                    </div>\n                    <div id="farButton" class="smart-scroll-button smart-arrow-right" role="presentation" aria-hidden="true"></div>\n            </div>' }
                static get listeners() { return { "nearButton.click": "_nearButtonClickHandler", "nearButton.down": "_startRepeat", "nearButton.up": "_stopRepeat", "nearButton.pointerenter": "_updateInBoundsFlag", "nearButton.pointerleave": "_updateInBoundsFlag", "farButton.click": "_farButtonClickHandler", "farButton.down": "_startRepeat", "farButton.up": "_stopRepeat", "farButton.pointerenter": "_updateInBoundsFlag", "farButton.pointerleave": "_updateInBoundsFlag", "track.down": "_trackDownHandler", "track.click": "_trackClickHandler", "track.move": "_trackMoveHandler", "thumb.down": "_dragStartHandler", "document.move": "_dragHandler", "document.up": "_dragEndHandler", up: "_dragEndHandler", "document.selectstart": "_selectStartHandler", resize: "_resizeHandler" } }
                _updateInBoundsFlag(t) {
                    const e = this,
                        a = t.target;
                    a._isPointerInBounds = !0, -1 !== t.type.indexOf("leave") && (a._isPointerInBounds = !1), 1 !== ("buttons" in t ? t.buttons : t.which) && e._stopRepeat(t)
                }
                _startRepeat(t) {
                    const e = this;
                    if (e.disabled) return;
                    const a = t.target;
                    a._initialTimer || (a._initialTimer = setTimeout((function() {
                        a._repeatTimer = setInterval((() => {
                            if (a._isPointerInBounds) {
                                const e = "buttons" in t ? t.buttons : t.which;
                                a.$.fireEvent("click", { buttons: e, clientX: t.clientX, clientY: t.clientY, pageX: t.pageX, pageY: t.pageY, screenX: t.screenX, screenY: t.screenY })
                            }
                        }), e.clickRepeatDelay)
                    }), 3 * e.clickRepeatDelay))
                }
                _stopRepeat(t) {
                    if (this.disabled) return;
                    const e = t.target;
                    e._repeatTimer && (clearInterval(e._repeatTimer), e._repeatTimer = null), e._initialTimer && (clearTimeout(e._initialTimer), e._initialTimer = null)
                }
                _calculateThumbSize(t) {
                    const e = this,
                        a = e.max - e.min,
                        r = "horizontal" === e.orientation ? e.$.track.offsetWidth > 10 : e.$.track.offsetHeight > 10;
                    let n = 0;
                    return a >= 1 && r ? (n = t / (a + t) * t, e.$.thumb.className.indexOf("smart-hidden") >= 0 && e.$thumb.removeClass("smart-hidden")) : e.$thumb.addClass("smart-hidden"), Math.max(10, Math.min(n, t))
                }
                _dragStartHandler(t) {
                    const e = this;
                    e.disabled || (e.thumbCapture = !0, e.dragStartX = t.clientX, e.dragStartY = t.clientY, e.dragStartValue = e.value, t.stopPropagation(), t.preventDefault())
                }
                _dragHandler(t) {
                    const e = this;
                    if (!0 !== e.thumbCapture) return;
                    e._isThumbDragged = !0;
                    const a = (e.max - e.min) / (e.scrollBarSize - e.thumbSize),
                        r = "horizontal" === e.orientation ? (t.clientX - e.dragStartX) * a : (t.clientY - e.dragStartY) * a;
                    let n = r;
                    e.rightToLeft && "horizontal" === e.orientation && (n = -r), e._updateValue(e.dragStartValue + n), t.stopPropagation(), t.preventDefault(), t.originalEvent && (t.originalEvent.stopPropagation(), t.originalEvent.preventDefault())
                }
                _dragEndHandler(t) {
                    const e = this;
                    e._trackDownTimer && (clearInterval(e._trackDownTimer), e._trackDownTimer = null), e.thumbCapture && (e.thumbCapture = !1, e._isThumbDragged = !1, "switchWhenReleased" === e.mechanicalAction ? e._updateValue(e.dragStartValue, e.value) : "switchUntilReleased" === this.mechanicalAction && e._updateValue(e.dragStartValue), t.preventDefault(), t.stopPropagation(), t.originalEvent.preventDefault(), t.originalEvent.stopPropagation())
                }
                _farButtonClickHandler() {
                    const t = this;
                    if (t.disabled) return;
                    const e = t.value;
                    t._updateValue(t.value + ("horizontal" === t.orientation && t.rightToLeft ? -1 : 1) * t.step), "switchUntilReleased" === t.mechanicalAction && t._updateValue(e)
                }
                _nearButtonClickHandler() {
                    const t = this;
                    if (t.disabled) return;
                    const e = t.value;
                    t._updateValue(t.value - ("horizontal" === t.orientation && t.rightToLeft ? -1 : 1) * t.step), "switchUntilReleased" === t.mechanicalAction && t._updateValue(e)
                }
                propertyChangedHandler(t, e, a) {
                    super.propertyChangedHandler(t, e, a);
                    const r = this;
                    switch (t) {
                        case "min":
                        case "max":
                        case "orientation":
                        case "showButtons":
                            r._layout(), "min" === t ? r.setAttribute("aria-valuemin", a) : "max" === t ? r.setAttribute("aria-valuemax", a) : "orientation" === t && r.setAttribute("aria-orientation", a);
                            break;
                        case "value":
                            r._updateValue(e, a);
                            break;
                        default:
                            r._layout()
                    }
                }
                render() {
                    const t = this;
                    t.setAttribute("role", "scrollbar"), t.setAttribute("aria-orientation", t.orientation), t.setAttribute("aria-valuemin", t.min), t.setAttribute("aria-valuemax", t.max), t.setAttribute("aria-valuenow", t.value), t._layout(), super.render()
                }
                _resizeHandler() { this._layout() }
                refresh() { this._layout() }
                beginUpdate() { this._isUpdating = !0 }
                endUpdate() { this._isUpdating = !1, this.refreshValue() }
                refreshValue() {
                    const t = this;
                    t._layout(), t._updateValue(t.value)
                }
                _layout() {
                    const t = this;
                    t._isUpdating || (t.scrollBarSize = "horizontal" === t.orientation ? t.$.track.offsetWidth : t.$.track.offsetHeight, t.thumbSize = t._calculateThumbSize(t.scrollBarSize), "horizontal" === t.orientation && t.$.thumb.style.width !== t.thumbSize + "px" ? t.$.thumb.style.width = t.thumbSize + "px" : "vertical" === t.orientation && t.$.thumb.style.height !== t.thumbSize + "px" && (t.$.thumb.style.height = t.thumbSize + "px"), "horizontal" === t.orientation ? (t.$.nearButton.classList.contains("smart-arrow-up") && t.$.nearButton.classList.remove("smart-arrow-up"), t.$.farButton.classList.contains("smart-arrow-down") && t.$.farButton.classList.remove("smart-arrow-down"), t.$.nearButton.classList.contains("smart-arrow-left") || t.$.nearButton.classList.add("smart-arrow-left"), t.$.farButton.classList.contains("smart-arrow-right") || t.$.farButton.classList.add("smart-arrow-right")) : (t.$.nearButton.classList.contains("smart-arrow-left") && t.$.nearButton.classList.remove("smart-arrow-left"), t.$.farButton.classList.contains("smart-arrow-right") && t.$.farButton.classList.remove("smart-arrow-right"), t.$.nearButton.classList.contains("smart-arrow-up") || t.$.nearButton.classList.add("smart-arrow-up"), t.$.farButton.classList.contains("smart-arrow-down") || t.$.farButton.classList.add("smart-arrow-down")), t._updateThumbPosition(), (t.value > t.max || t.value < t.min) && t._updateValue(t.value, t.value > t.max ? t.max : t.min))
                }
                _selectStartHandler(t) { this.thumbCapture && t.preventDefault() }
                _trackDownHandler(t) {
                    const e = this;
                    t.target === e.$.track && (e._trackDownTimer && clearInterval(e._trackDownTimer), e.thumbCapture || (e._trackDownTimer = setInterval((function() { e._trackClickHandler(t) }), e.clickRepeatDelay), t.stopPropagation(), t.preventDefault()))
                }
                _trackClickHandler(t) {
                    const e = this;
                    if (e.disabled) return;
                    if (e._isThumbDragged) return clearInterval(e._trackDownTimer), void(e._trackDownTimer = null);
                    const a = e.$.thumb.getBoundingClientRect(),
                        r = t.pageX - window.pageXOffset,
                        n = t.pageY - window.pageYOffset,
                        i = (e.rightToLeft ? -1 : 1) * e.value;
                    "horizontal" === e.orientation ? r > (e._isThumbDragged ? e.dragStartX : a.right) ? e._updateValue(e.value + (e.rightToLeft ? -1 : 1) * e.largeStep) : r < (e._isThumbDragged ? e.dragStartX : a.left) && e._updateValue(e.value - (e.rightToLeft ? -1 : 1) * e.largeStep) : n > (e._isThumbDragged ? e.dragStartY : a.bottom) ? e._updateValue(e.value + e.largeStep) : n < (e._isThumbDragged ? e.dragStartY : a.top) && e._updateValue(e.value - e.largeStep), "switchUntilReleased" === e.mechanicalAction && e._updateValue(i)
                }
                _trackMoveHandler(t) { "touchmove" === t.originalEvent.type && t.originalEvent.preventDefault() }
                _updateValue(t, e) {
                    const a = this;
                    if (!a._isUpdating && (1 === arguments.length && (e = t, t = a.value), (void 0 === e || isNaN(e)) && (e = a.min), e > a.max && (e = a.max), e < a.min && (e = a.min), a.value = e, t !== e)) {
                        if (a.setAttribute("aria-valuenow", e), a._updateThumbPosition(), a.thumbCapture && "switchWhenReleased" === a.mechanicalAction) return;
                        if (a.onChange) return void a.onChange({ value: a.value, oldValue: t, min: a.min, max: a.max, context: a });
                        a.$.fireEvent("change", { value: a.value, oldValue: t, min: a.min, max: a.max })
                    }
                }
                _updateThumbPosition() {
                    const t = this,
                        e = "horizontal" === t.orientation ? t.$.track.offsetWidth : t.$.track.offsetHeight,
                        a = t._calculateThumbSize(e),
                        r = e - a;
                    let n = (e - a) / (t.max - t.min) * (t.value - t.min);
                    t.rightToLeft && "horizontal" === t.orientation && (n = (e - a) / (t.max - t.min) * (t.max - t.value - t.min)), n = Math.min(r, Math.max(0, n)), "vertical" === t.orientation && t.$.thumb.style.top !== n + "px" ? t.$.thumb.style.top = n + "px" : "horizontal" === t.orientation && t.$.thumb.style.left !== n + "px" && (t.$.thumb.style.left = n + "px")
                }
            });

            /***/
        }),

        /***/
        5482:
        /***/
            (() => {

            Smart("smart-tree-item", class extends Smart.MenuItem {
                static get properties() { return { selected: { value: !1, type: "boolean" } } }
                ready() {
                    const e = this;
                    Object.defineProperty(e, "hasStyleObserver", { get: function() { return !1 } }), super.ready(), e.setAttribute("role", "treeitem"), e.setAttribute("aria-label", e.label)
                }
                propertyChangedHandler(e, t, r) {
                    const n = this,
                        l = n.menu;
                    if (super.propertyChangedHandler(e, t, r), "level" === e) return void(n.level = t);
                    if ("disabled" === e || "separator" === e || !l) return;
                    const a = l.context;
                    switch (l.context = l, e) {
                        case "label":
                            { const e = l.sorted && l.autoSort;n.firstElementChild.firstElementChild.firstElementChild.innerHTML = r, e && (l._unsortItems(l.$.mainContainer), l._applyGrouping(l.$.mainContainer)), l._state.filter && l._applyFilter(l._state.filter), n.setAttribute("aria-label", r); break }
                        case "selected":
                            n.selected = t, r ? l.select(n) : l.unselect(n);
                            break;
                        case "shortcut":
                            { let e = n.firstElementChild.children[1];e || (e = document.createElement("div"), e.className = "smart-tree-item-shortcut", n.firstElementChild.appendChild(e)), e.innerHTML = r; break }
                        case "value":
                            l.sort && l.sorted && l.autoSort && l._refreshSorting()
                    }
                    l.context = a
                }
                _setId() {}
            }), Smart("smart-tree-items-group", class extends Smart.MenuItemsGroup {
                static get properties() { return { selected: { value: !1, type: "boolean" } } }
                ready() {
                    const e = this;
                    Object.defineProperty(e, "hasStyleObserver", { get: function() { return !1 } }), super.ready(), e.setAttribute("role", "treeitem"), e.removeAttribute("aria-haspopup"), e.setAttribute("aria-label", e.label)
                }
                propertyChangedHandler(e, t, r) {
                    const n = this,
                        l = n.menu;
                    if (super.propertyChangedHandler(e, t, r), "level" === e) return void(n.level = t);
                    if ("disabled" === e || "separator" === e || !l) return;
                    const a = l.context;
                    switch (l.context = l, e) {
                        case "expanded":
                            n.expanded = t, r ? l.expandItem(n) : l.collapseItem(n);
                            break;
                        case "label":
                            { const e = l.sorted && l.autoSort;n.firstElementChild.firstElementChild.firstElementChild.innerHTML = r, e && (l._unsortItems(l.$.mainContainer), l._applyGrouping(l.$.mainContainer)), l._state.filter && l._applyFilter(l._state.filter), n.setAttribute("aria-label", r); break }
                        case "selected":
                            n.selected = t, r ? l.select(n) : l.unselect(n);
                            break;
                        case "value":
                            l.sort && l.sorted && l.autoSort && l._refreshSorting()
                    }
                    l.context = a
                }
                _setId() {}
            }), Smart("smart-tree", class extends Smart.Menu {
                static get properties() { return { allowDrag: { value: !1, type: "boolean" }, allowDrop: { value: !1, type: "boolean" }, autoHideToggleElement: { value: !1, type: "boolean" }, autoLoadState: { value: !1, type: "boolean" }, autoSaveState: { value: !1, type: "boolean" }, autoSort: { value: !0, type: "boolean" }, displayLoadingIndicator: { value: !1, type: "boolean" }, dragFeedbackFormatFunction: { value: null, type: "function?" }, dragOffset: { value: [10, 10], type: "array" }, editable: { value: !1, type: "boolean" }, expandMode: { value: "multiple", allowedValues: ["multiple", "single"], type: "string" }, filterable: { value: !1, type: "boolean" }, filterInputPlaceholder: { value: "", type: "string" }, filterMember: { value: "label", type: "string" }, filterMode: { value: "containsIgnoreCase", allowedValues: ["contains", "containsIgnoreCase", "doesNotContain", "doesNotContainIgnoreCase", "equals", "equalsIgnoreCase", "startsWith", "startsWithIgnoreCase", "endsWith", "endsWithIgnoreCase"], type: "string" }, hasThreeStates: { value: !1, type: "boolean" }, loadingIndicatorPlaceholder: { value: "Loading...", type: "string" }, loadingIndicatorPosition: { value: "center", allowedValues: ["bottom", "center", "top"], type: "string" }, messages: { value: { en: { noId: "smart-tree: Saving and loading the element's state are not available if the element has no id." } }, type: "object", extend: !0 }, scrollMode: { value: "scrollbar", allowedValues: ["scrollbar", "scrollButtons"], type: "string" }, selectedIndexes: { value: [], type: "array" }, selectionDisplayMode: { value: "row", allowedValues: ["row", "label"], type: "string" }, selectionMode: { value: "one", allowedValues: ["none", "oneOrManyExtended", "zeroOrMany", "oneOrMany", "zeroOrOne", "zeroAndOne", "one", "checkBox", "radioButton"], type: "string" }, selectionTarget: { value: "all", allowedValues: ["all", "leaf"], type: "string" }, showLines: { value: !1, type: "boolean" }, showRootLines: { value: !1, type: "boolean" }, sort: { value: null, type: "function?", reflectToAttribute: !1 }, sortDirection: { value: "asc", allowedValues: ["asc", "desc"], type: "string" }, sorted: { value: !1, type: "boolean" }, toggleElementPosition: { value: "near", allowedValues: ["near", "far"], type: "string" }, toggleMode: { value: "dblclick", allowedValues: ["click", "dblclick", "arrow"], type: "string" } } }
                static get listeners() { return { blur: "_blurHandler", focus: "_focusHandler", keydown: "_keydownHandler", mouseenter: "_mouseenterHandler", mouseleave: "_mouseleaveHandler", resize: "_checkOverflow", styleChanged: "_styleChangedHandler", transitionend: "_overriddenMenuHandler", "container.click": "_overriddenMenuHandler", "container.mouseout": "_overriddenMenuHandler", "container.mouseover": "_overriddenMenuHandler", "container.pointerover": "_pointeroverHandler", "editInput.blur": "_editInputBlurHandler", "filterInput.keydown": "_filterInputKeydownHandler", "filterInput.keyup": "_filterInputKeyupHandler", "mainContainer.click": "_overriddenMenuHandler", "mainContainer.mouseleave": "_overriddenMenuHandler", "mainContainer.mouseout": "_overriddenMenuHandler", "mainContainer.mouseover": "_overriddenMenuHandler", "mainContainer.swipeleft": "_mainContainerSwipeHandler", "mainContainer.swiperight": "_mainContainerSwipeHandler", "scrollButtonFar.click": "_scrollButtonFarClickHandler", "scrollButtonNear.click": "_scrollButtonNearClickHandler", "scrollViewer.down": "_scrollViewerDownHandler", "scrollViewer.kineticScroll": "_scrollViewerWheelHandler", "scrollViewer.touchmove": "_scrollViewerTouchmoveHandler", "mainContainer.wheel": "_scrollViewerWheelHandler", "document.move": "_moveHandler", "document.selectstart": "_selectstartHandler", "document.up": "_documentUpHandler" } }
                static get requires() { return { "Smart.ScrollBar": "smart.scrollbar.js" } }
                static get styleUrls() { return ["smart.scrollbar.css", "smart.scrollviewer.css", "smart.tree.css"] }
                template() { return '<div id="container" role="presentation">\n                    <div class="smart-tree-filter-input-container" role="presentation"><input id="filterInput" class="smart-filter-input" disabled="[[disabled]]" placeholder="[[filterInputPlaceholder]]" type="text" role="searchbox" aria-label="[[filterInputPlaceholder]]" /></div>\n                    <smart-repeat-button id="scrollButtonNear" class="smart-tree-scroll-button smart-spin-button smart-scroll-button-near smart-hidden" animation="[[animation]]" unfocusable aria-label="Scroll up">\n                        <div id="arrowNear" class="smart-arrow smart-arrow-up"></div>\n                    </smart-repeat-button>\n                    <smart-scroll-viewer id="scrollViewer" animation="[[animation]]" horizontal-scroll-bar-visibility="hidden" right-to-left="[[rightToLeft]]">\n                        <div id="mainContainer" inner-h-t-m-l=\'[[innerHTML]]\' class="smart-tree-main-container" role="presentation">\n                            <content></content>\n                        </div>\n                        <input type="text" id="editInput" class="smart-tree-edit-input smart-hidden" />\n                    </smart-scroll-viewer>\n                    <smart-repeat-button id="scrollButtonFar" class="smart-tree-scroll-button smart-spin-button smart-scroll-button-far smart-hidden" animation="[[animation]]" unfocusable aria-label="Scroll down">\n                        <div id="arrowFar" class="smart-arrow smart-arrow-down"></div>\n                    </smart-repeat-button>\n                    <div id="loadingIndicatorContainer" class="smart-loader-container smart-hidden" role="presentation">\n                        <span id="loadingIndicator" class="smart-loader" role="img" aria-label="[[loadingIndicatorPlaceholder]]"></span>\n                        <span id="loadingIndicatorPlaceHolder" class="smart-loader-label smart-hidden">[[loadingIndicatorPlaceholder]]</span>\n                    </div>\n                </div>' }
                detached() {
                    const e = this,
                        t = e._dragDetails;
                    if (super.detached(), !t) return;
                    const r = Smart.Tree.hoveredTree,
                        n = Smart.Tree.hoveredItem;
                    delete e._dragDetails, delete Smart.Tree.treeItemDragged, delete Smart.Tree.hoveredTree, delete Smart.Tree.hoveredItem, e.$.scrollViewer._scrollView.disableSwipeScroll = !1, t.FeedbackShown && (n.classList.remove("drop-target", "top", "bottom"), document.body.classList.remove("smart-dragging"), t.Feedback.remove(), r && clearInterval(r._dragInterval))
                }
                addAfter(e, t) { void 0 !== (t = this.getItem(t)) && this.addTo(e, t.parentItem, t, !0) }
                addBefore(e, t) { void 0 !== (t = this.getItem(t)) && this.addTo(e, t.parentItem, t) }
                addTo(e, t) {
                    const r = this;
                    if (!(e instanceof Smart.TreeItem || e instanceof Smart.TreeItemsGroup))
                        if ("string" == typeof e) {
                            const t = document.createElement("smart-tree-item");
                            t.label = e, e = t
                        } else {
                            if (!e || !e.label) return; {
                                const t = document.createElement("smart-tree-item");
                                t.label = e.label, e = t
                            }
                        }
                    let n, l;
                    if (e.isDirty = !1, void 0 === t) n = 1, l = t = r.$.mainContainer;
                    else {
                        if ((t = r.getItem(t)) instanceof Smart.TreeItemsGroup == 0) return;
                        n = t.level + 1, l = t.itemContainer
                    }
                    r._createItemHTMLStructure(e, n, t, l.childElementCount, 0);
                    const a = r.sorted && r.autoSort,
                        o = r._state.filter,
                        s = r.selectedIndexes.slice(0);
                    a && r._unsortItems(r.$.mainContainer), e instanceof Smart.TreeItemsGroup && (Array.from(e.querySelectorAll("smart-tree-item, smart-tree-items-group")).forEach((e => e.isDirty = !1)), r._processHTML(e, n + 1, !1));
                    let i = arguments[2];
                    i && arguments[3] && (i = i.nextElementSibling), i ? (l.insertBefore(e, i), r._menuItems = {}, r._refreshItemPaths(r.$.mainContainer, !0, void 0, r.sorted && !r.autoSort)) : l.appendChild(e), a && r._applyGrouping(r.$.mainContainer), o && r._applyFilter(o), r._checkOverflow(), r._expandItemsByDefault(), r.selectedIndexes = [], r._applySelection(!0, s)
                }
                getSelectedValues() {
                    const e = this,
                        t = [];
                    for (let r = 0; r < e.selectedIndexes.length; r++) {
                        const n = e._menuItems[e.selectedIndexes[r]];
                        n.hasAttribute("value") ? t.push(n.getAttribute("value")) : n.hasAttribute("label") && t.push(n.getAttribute("label"))
                    }
                    return t
                }
                unselectValues(e) {
                    const t = this;
                    e && Object.keys(t._menuItems).forEach((r => {
                        const n = t._menuItems[r];
                        let l = null;
                        n.hasAttribute("value") ? l = n.getAttribute("value") : n.hasAttribute("label") && (l = n.getAttribute("label")), "string" == typeof e ? e === l && t.unselect(r) : e.indexOf(l) >= 0 && t.unselect(r)
                    }))
                }
                setSelectedValues(e) {
                    const t = this;
                    e && Object.keys(t._menuItems).forEach((r => {
                        const n = t._menuItems[r];
                        let l = null;
                        n.hasAttribute("value") ? l = n.getAttribute("value") : n.hasAttribute("label") && (l = n.getAttribute("label")), "string" == typeof e ? e === l && t._canItemBeSelected(n) && t._handleSelection(n, { type: "programmatic" }) : e.indexOf(l) >= 0 && t._canItemBeSelected(n) && t._handleSelection(n, { type: "programmatic" })
                    }))
                }
                clearSelection() {
                    const e = this,
                        t = e.selectedIndexes.slice(0);
                    e.selectedIndexes = [], e._applySelection(!1, t)
                }
                collapseAll(e) {
                    const t = this,
                        r = t.animation,
                        n = !1 === e && t.hasAnimation;
                    n && (t.animation = "none"), t._collapseAll(!0), n && (t.animation = r)
                }
                ensureVisible(e) {
                    const t = this;
                    if (void 0 === (e = t.getItem(e)) || e.hidden) return;
                    let r = !1;
                    e.level > 1 && !t._isBranchExpanded(e) && (super.expandItem(e.parentItem, void 0, !0), r = t.hasAnimation, r && (t._ensureVisibleOnTransitionend = e)), r || t._ensureVisible(e)
                }
                expandAll(e) {
                    const t = this,
                        r = t.animation,
                        n = !1 === e && t.hasAnimation;
                    let l = 1,
                        a = (t.enableShadowDOM ? t.shadowRoot : t).querySelectorAll('smart-tree-items-group[level="1"]');
                    for (n && (t.animation = "none"); a.length > 0;) {
                        for (let e = 0; e < a.length; e++) {
                            const r = a[e];
                            r.expanded || t._menuItemsGroupSelectionHandler(r, { target: r, type: "expand" })
                        }
                        l++, a = (t.enableShadowDOM ? t.shadowRoot : t).querySelectorAll('smart-tree-items-group[level="' + l + '"]')
                    }
                    n && (t.animation = r)
                }
                expandItem(e, t) {
                    const r = this;
                    if (void 0 === (e = r.getItem(e)) || e instanceof Smart.TreeItemsGroup == 0 || e && e.container && r._isContainerOpened(e.container.level, e.container)) return;
                    void 0 !== Smart.Menu.processTimer && r._lazyInitItems();
                    const n = !1 === t && r.hasAnimation,
                        l = r.animation;
                    n && (r.animation = "none"), r._discardKeyboardHover(), r._menuItemsGroupSelectionHandler(e, { target: e, type: "expand" }, arguments[2]), n && (r.animation = l)
                }
                filter(e) {
                    const t = this;
                    t.filterable && (t._applyFilter(e), t.$.filterInput.value = e)
                }
                getState() { return JSON.parse(JSON.stringify(this._state)) }
                insert(e, t) {
                    const r = this;
                    let n;
                    if (e instanceof Smart.TreeItem || e instanceof Smart.TreeItemsGroup) {
                        if (r.contains(e)) return;
                        e.isDirty = !1, n = e
                    } else {
                        if ("object" != typeof e || e.constructor !== Object) return;
                        n = function e(t) {
                            const n = t[r.itemsMember],
                                l = "smart-tree-items-group" === t.tagName || Array.isArray(n) ? "smart-tree-items-group" : "smart-tree-item",
                                a = document.createElement(l);
                            if (a.isDirty = !1, t.disabled && (a.disabled = !0), t[r.displayMember] && (a.label = t[r.displayMember]), t.selected && (a.selected = !0), t.separator && (a.separator = !0), t[r.valueMember] && (a.value = t[r.valueMember]), "smart-tree-items-group" === l) {
                                if (t.expanded && (a.expanded = !0), n)
                                    for (let t = 0; t < n.length; t++) a.appendChild(e(n[t]))
                            } else t.shortcut && (a.shortcut = t.shortcut);
                            return a
                        }(e)
                    }
                    if (void 0 === t) return void r.addTo(n);
                    if ("number" == typeof t) t = t.toString();
                    else if (t instanceof Smart.TreeItem || t instanceof Smart.TreeItemsGroup) {
                        if (!r.contains(t)) return;
                        t = t.path
                    } else if ("string" != typeof t) return;
                    const l = t.split(".");
                    let a, o;
                    1 === l.length ? (o = r._menuItems[l[0]], o ? r.addBefore(n, o) : r.addTo(n)) : (o = r._menuItems[t], a = r._menuItems[l.slice(0, l.length - 1).join(".")], o ? r.addBefore(n, o) : a && a instanceof Smart.TreeItemsGroup && r.addTo(n, a))
                }
                loadState(e) {
                    const t = this,
                        r = t.selectedIndexes.slice(0),
                        n = [];
                    if (!e) { if (!t.id) return void t.warn(t.localize("noId")); if (!(e = window.localStorage.getItem("smartTree" + t.id))) return }
                    "string" == typeof e && (e = JSON.parse(e)), e.filter && !t.filterable && (e.filter = "");
                    let l = e.filter !== t._state.filter;
                    e.sorted !== t.sorted ? (t.sorted = e.sorted, t._updateState("sorted", t.sorted), e.sorted ? t._applyGrouping(t.$.mainContainer) : t._unsortItems(t.$.mainContainer), (e.filter || l) && (t._applyFilter(e.filter), t.$.filterInput.value = e.filter)) : l && (t._applyFilter(e.filter), t.$.filterInput.value = e.filter), t._menuItemsGroupsToExpand = [];
                    for (let r = 0; r < e.expanded.length; r++) {
                        const n = t.getItem(e.expanded[r]);
                        n && t._menuItemsGroupsToExpand.push(n)
                    }
                    t._expandItemsByDefault(!0);
                    for (let r = 0; r < e.selected.length; r++) {
                        const l = t.getItem(e.selected[r]);
                        l && n.push(l.path)
                    }
                    t.selectedIndexes = n, t._applySelection(!1, r)
                }
                moveDown(e) {
                    const t = this,
                        r = (e = t.getItem(e)).nextElementSibling;
                    void 0 !== e && r && !t.sorted && (t._moveTreeItem(e, r, 2, [t]), t.filterable && t._state.filter && t._applyFilter(t._state.filter))
                }
                moveUp(e) {
                    const t = this,
                        r = (e = t.getItem(e)).previousElementSibling;
                    void 0 !== e && r && !t.sorted && (t._moveTreeItem(e, r, 0, [t]), t.filterable && t._state.filter && t._applyFilter(t._state.filter))
                }
                refresh() { this._checkOverflow() }
                removeItem(e) {
                    const t = this;
                    if (void 0 === (e = t.getItem(e))) return;
                    if (e instanceof Smart.TreeItemsGroup) {
                        const r = e.container;
                        t._isContainerOpened(r.level, r) && t._closeSubContainersTreeMode(r.level, r)
                    }
                    const r = t.sorted && t.autoSort;
                    r && t._unsortItems(t.$.mainContainer), e.parentElement.removeChild(e), t._menuItems = {}, t._refreshItemPaths(t.$.mainContainer, !0, void 0, t.sorted && !t.autoSort), r && t._applyGrouping(t.$.mainContainer);
                    const n = t._state.filter,
                        l = t.selectedIndexes.slice(0);
                    n && t._applyFilter(n), t._checkOverflow(), t.selectedIndexes = [], t._applySelection(!0, l), delete t._treeAnimationInProgress
                }
                saveState() { const e = this; return e.id ? window.localStorage.setItem("smartTree" + e.id, JSON.stringify(e._state)) : e.warn(e.localize("noId")), JSON.parse(JSON.stringify(e._state)) }
                select(e) {
                    const t = this;
                    void 0 !== (e = t.getItem(e)) && !e.selected && t._canItemBeSelected(e) && t._handleSelection(e, { type: "programmatic" })
                }
                unselect(e) { void 0 !== (e = this.getItem(e)) && e.selected && !e.templateApplied && this._handleSelection(e, { type: "programmatic" }) }
                updateItem(e, t) {
                    if (void 0 === (e = this.getItem(e)) || void 0 === t) return;
                    const r = e instanceof Smart.TreeItem;
                    for (let n in t)
                        if (Object.prototype.hasOwnProperty.call(t, n)) {
                            if (r) { if (-1 === ["disabled", "label", "level", "selected", "separator", "shortcut", "value"].indexOf(n)) continue } else if (-1 === ["disabled", "expanded", "label", "level", "selected", "separator", "value"].indexOf(n)) continue;
                            e[n] = t[n]
                        }
                }
                propertyChangedHandler(e, t, r) {
                    const n = this;
                    switch (super.propertyChangedHandler(e, t, r), e) {
                        case "allowDrag":
                        case "allowDrop":
                        case "autoLoadState":
                        case "autoSort":
                        case "editable":
                        case "filterInputPlaceholder":
                        case "loadingIndicatorPlaceholder":
                        case "selectionDisplayMode":
                        case "showLines":
                        case "showRootLines":
                        case "toggleElementPosition":
                        case "toggleMode":
                            break;
                        case "autoHideToggleElement":
                            r ? n.$mainContainer.addClass("hidden-arrows") : n.$mainContainer.removeClass("hidden-arrows");
                            break;
                        case "autoSaveState":
                            if (!r) return;
                            if (!n.id) return n.warn(n.localize("noId")), void(n.autoSaveState = !1);
                            window.localStorage.setItem("smartTree" + n.id, JSON.stringify(n._state));
                            break;
                        case "dataSource":
                            { const e = n.selectedIndexes.slice(0);n.selectedIndexes = [], n._menuItems = {}, n._processDataSource(), n._checkOverflow(), n._expandItemsByDefault(), n._applySelection(!0, e); const t = n._state.filter;t && n._applyFilter(t); break }
                        case "disabled":
                            n._setFocusable(), n.$.scrollButtonNear.disabled = r, n.$.scrollButtonFar.disabled = r, r || n._updateScrollButtonVisibility();
                            break;
                        case "displayLoadingIndicator":
                            r ? (n._discardKeyboardHover(!0), n.$loadingIndicatorContainer.removeClass("smart-hidden")) : n.$loadingIndicatorContainer.addClass("smart-hidden");
                            break;
                        case "expandMode":
                            if ("single" === r) {
                                const e = n._state.expanded.map((e => Object.values(n._menuItems).find((t => t.id === e)))),
                                    t = {};
                                for (let r = 0; r < e.length; r++) {
                                    const l = e[r],
                                        a = l.parentItem;
                                    if (t[a]) continue;
                                    t[a] = !0;
                                    const o = e.filter((e => e !== l && e.parentItem === a));
                                    o.length > 0 && o.forEach((e => n.collapseItem(e)))
                                }
                            }
                            break;
                        case "filterable":
                            !1 === r && (n._applyFilter(""), n.$.filterInput.value = ""), n._checkOverflow();
                            break;
                        case "filterMode":
                            n.filterable && n._state.filter && n._applyFilter(n._state.filter);
                            break;
                        case "hasThreeStates":
                            if ("checkBox" !== n.selectionMode) return;
                            if (r) n._applySelection(!1);
                            else { const e = (n.enableShadowDOM ? n.shadowRoot : n).querySelectorAll("[indeterminate]"); for (let t = 0; t < e.length; t++) e[t].removeAttribute("indeterminate") }
                            break;
                        case "innerHTML":
                            n.$.mainContainer.innerHTML = r, n._lazyInitItems();
                            break;
                        case "loadingIndicatorPosition":
                            "center" === r ? n.$loadingIndicatorPlaceHolder.addClass("smart-hidden") : n.$loadingIndicatorPlaceHolder.removeClass("smart-hidden");
                            break;
                        case "overflow":
                            if ("scrollbar" === n.scrollMode) return "hidden" === r ? n.$.scrollViewer.$.verticalScrollBar.setAttribute("aria-hidden", !0) : n.$.scrollViewer.$.verticalScrollBar.removeAttribute("aria-hidden"), void(n.$.scrollViewer.verticalScrollBarVisibility = "scroll" === r ? "visible" : "auto");
                            n.$.scrollViewer.scrollTop = 0, "hidden" === r ? (n.$scrollViewer.removeClass("scroll-buttons-shown"), n.$scrollButtonNear.addClass("smart-hidden"), n.$scrollButtonFar.addClass("smart-hidden")) : (n.$.scrollButtonNear.disabled = n.disabled, n.$.scrollButtonFar.disabled = n.disabled, "auto" === r ? (n.$scrollButtonNear.addClass("smart-hidden"), n.$scrollButtonFar.addClass("smart-hidden"), n._checkOverflow()) : (n.$scrollViewer.addClass("scroll-buttons-shown"), n.$scrollViewer.removeClass("one-button-shown"), n.$scrollButtonNear.removeClass("smart-hidden"), n.$scrollButtonFar.removeClass("smart-hidden"), n._updateScrollButtonVisibility())), n.$.scrollViewer.refresh();
                            break;
                        case "rightToLeft":
                            {
                                let e, t;r ? (e = "paddingLeft", t = "paddingRight") : (e = "paddingRight", t = "paddingLeft");
                                for (let r in n._menuItems)
                                    if (Object.prototype.hasOwnProperty.call(n._menuItems, r)) {
                                        const l = n._menuItems[r],
                                            a = l.firstElementChild;
                                        a.style[e] = "", n._setIndentation(a, l.level, t)
                                    }
                                break
                            }
                        case "scrollMode":
                            if ("hidden" === n.overflow) return;
                            if (n.$.scrollViewer.scrollTop = 0, "scrollButtons" === r) return "scroll" === n.overflow && (n.$scrollViewer.addClass("scroll-buttons-shown"), n.$scrollButtonNear.removeClass("smart-hidden"), n.$scrollButtonFar.removeClass("smart-hidden")), n.$.scrollViewer.$.verticalScrollBar.setAttribute("aria-hidden", !0), n.$.scrollViewer.verticalScrollBarVisibility = "auto", void n._checkOverflow();
                            n.$.scrollViewer.$.verticalScrollBar.removeAttribute("aria-hidden"), n.$scrollViewer.removeClass("scroll-buttons-shown"), n.$scrollViewer.removeClass("one-button-shown"), n.$scrollButtonNear.addClass("smart-hidden"), n.$scrollButtonFar.addClass("smart-hidden"), "auto" === n.overflow ? n.$.scrollViewer.verticalScrollBarVisibility = "auto" : n.$.scrollViewer.verticalScrollBarVisibility = "visible";
                            break;
                        case "selectedIndexes":
                            n._applySelection(!1, t);
                            break;
                        case "selectionMode":
                            if (n.setAttribute("aria-multiselectable", -1 !== ["oneOrManyExtended", "zeroOrMany", "oneOrMany", "checkBox", "radioButton"].indexOf(r)), void 0 === n._menuItems[0]) return;
                            if ("one" === t && "none" !== r && "checkBox" !== r && "radioButton" !== r || -1 !== t.indexOf("oneOrMany") && -1 !== r.indexOf("oneOrMany") || "none" === t && (-1 !== r.indexOf("zero") || "checkBox" === r) || "zeroOrMany" === r && "checkBox" !== t || "radioButton" === t && -1 !== r.indexOf("Many") || !n.hasThreeStates && ("checkBox" === r || "checkBox" === t && "zeroOrMany" === r)) return n._lastSelectedItem = "one" === r || "oneOrManyExtended" === r ? n._menuItems[n.selectedIndexes[n.selectedIndexes.length - 1]] : void 0, void n._applyAriaSelected();
                            if (n.hasThreeStates && "checkBox" === t) { const e = (n.enableShadowDOM ? n.shadowRoot : n).querySelectorAll("[indeterminate]"); for (let t = 0; t < e.length; t++) e[t].removeAttribute("indeterminate") }
                            n._applySelection(!1);
                            break;
                        case "sort":
                            if (!n.sorted) return;
                            n._refreshSorting();
                            break;
                        case "sortDirection":
                            n.sorted && !n.sort && (n._unsortItems(n.$.mainContainer), n._applyGrouping(n.$.mainContainer));
                            break;
                        case "sorted":
                            { if (!r && !n.autoSort) return n._refreshItemPathsAndSelection(), void n._updateState("sorted", !1);r ? n._applyGrouping(n.$.mainContainer) : n._unsortItems(n.$.mainContainer); const e = n._state.filter;e && n._applyFilter(e), n._updateState("sorted", r), n._checkOverflow(); break }
                        case "unfocusable":
                            n._setFocusable()
                    }
                }
                _addDragFeedback() {
                    const e = this,
                        t = document.createElement("div");
                    return t.className = "smart-tree-item-feedback", t.setAttribute("parent-tree-id", e.id), e.theme && t.setAttribute("theme", e.theme), e.dragFeedbackFormatFunction ? t.innerHTML = e.dragFeedbackFormatFunction(e._dragDetails.Items) : 1 === e._dragDetails.Items.length ? t.innerHTML = e._dragDetails.Item.label : (t.classList.add("multiple"), t.innerHTML = "&#xf0c5;"), document.body.appendChild(t), t
                }
                _applyFilter(e) {
                    const t = this;

                    function r(e, t) { e ? (t.hidden && t.$.removeClass("smart-hidden"), t.hidden = !1) : (t.hidden || t.$.addClass("smart-hidden"), t.hidden = !0) }
                    if ("" === e && !t.hasAttribute("filter-applied")) return;
                    const n = Array.from(t.$.mainContainer.getElementsByClassName("last-filtered-child"));
                    for (let e = 0; e < n.length; e++) n[e].$.removeClass("last-filtered-child");
                    ! function n(l, a) {
                        let o, s = !1,
                            i = 0;
                        a = Array.from(a);
                        for (let l = 0; l < a.length; l++) {
                            const d = a[l];
                            d instanceof Smart.TreeItem ? r(t._findItem(d, e), d) : n(d, d.itemContainer.children), d.hidden || (i++, o = d), s = s || !d.hidden
                        }
                        if (l !== t.$.mainContainer) {
                            const n = t._findItem(l, e);
                            r(s || n, l), s && null === n ? l.$.addClass("filtered-child") : l.$.removeClass("filtered-child"), !s && a.length > 0 ? (l.hiddenChildren = !0, l.$.addClass("hidden-children"), t.collapseItem(l, void 0, !1)) : (l.hiddenChildren = !1, l.$.removeClass("hidden-children"))
                        }
                        "" !== e && i > 0 && o.$.addClass("last-filtered-child")
                    }(t.$.mainContainer, t.$.mainContainer.children), "" !== e ? t.setAttribute("filter-applied", "") : t.removeAttribute("filter-applied"), t._updateState("filter", e), t._checkOverflow()
                }
                _applyHierarchicalSelection(e, t) {
                    const r = this,
                        n = e !== r.$.mainContainer,
                        l = n ? e.itemContainer.children : e.children;
                    let a = 0,
                        o = 0;
                    for (let s = 0; s < l.length; s++) {
                        const i = l[s];
                        e.selected && i.set("selected", !0), i instanceof Smart.TreeItemsGroup ? r._applyHierarchicalSelection(i, t) : i.selected && t.push(i.path), n && (i.selected ? a++ : i.hasAttribute("indeterminate") && o++)
                    }
                    n && (r._setThreeStateCheckbox(e, a, o), e.selected && t.push(e.path))
                }
                _applyRadioButtonSelection(e, t, r) {
                    const n = this,
                        l = e !== n.$.mainContainer ? e.itemContainer.children : e.children,
                        a = [];
                    let o;
                    for (let e = 0; e < l.length; e++) {
                        const o = l[e];
                        o instanceof Smart.TreeItemsGroup && n._applyRadioButtonSelection(o, t, r), o.set("selected", !1), -1 !== t.indexOf(o.path) && a.push(o)
                    }
                    o = 0 === a.length ? l[0] : a[a.length - 1], o.set("selected", !0), r.push(o.path)
                }
                _applySelection(e, t) {
                    const r = this;
                    let n = r.selectedIndexes.slice(0);

                    function l(e) {
                        const t = Object.values(r._menuItems).filter((t => t.level === e));
                        if (0 !== t.length) {
                            for (let e = 0; e < t.length; e++)
                                if (r._canItemBeSelected(t[e])) return t[e].path;
                            return l(e + 1)
                        }
                    }
                    if (void 0 === t && (t = n.slice(0)), void 0 === r._menuItems[0]) return r.selectedIndexes = [], r._lastSelectedItem = void 0, void(r.isRendered && JSON.stringify(t) !== JSON.stringify([]) && r.$.fireEvent("change", { selectedIndexes: r.selectedIndexes, oldSelectedIndexes: t }));
                    const a = r.selectionMode,
                        o = Array.from((r.shadowRoot || r).querySelectorAll("smart-tree-item[selected], smart-tree-items-group[selected]"));
                    for (let e = n.length - 1; e >= 0; e--) {
                        const t = r._menuItems[n[e]];
                        void 0 !== t && r._canItemBeSelected(t) || n.splice(e, 1)
                    }
                    if (e)
                        for (let e = 0; e < o.length; e++) r._canItemBeSelected(o[e]) ? -1 === n.indexOf(o[e].path) && n.push(o[e].path) : o[e].set("selected", !1);
                    else {
                        for (let e = 0; e < o.length; e++) o[e].set("selected", !1);
                        o.length = 0
                    }
                    switch (r._sortPathCollection(n), a) {
                        case "none":
                            n.length = 0;
                            for (let e = 0; e < o.length; e++) o[e].set("selected", !1);
                            break;
                        case "one":
                        case "zeroAndOne":
                        case "zeroOrOne":
                            "one" === a && 0 === n.length && n.push(l(1));
                            for (let e = 0; e < n.length; e++) { const t = r._menuItems[n[e]]; if (e === n.length - 1) { t.set("selected", !0), n = [n[e]]; break } - 1 !== o.indexOf(t) && t.set("selected", !1) }
                            break;
                        case "oneOrMany":
                        case "oneOrManyExtended":
                            0 === n.length && n.push(l(1));
                            for (let e = 0; e < n.length; e++) r._menuItems[n[e]].set("selected", !0);
                            break;
                        case "zeroOrMany":
                        case "checkBox":
                            for (let e = 0; e < n.length; e++) r._menuItems[n[e]].set("selected", !0);
                            if ("checkBox" === a && r.hasThreeStates) {
                                const e = [];
                                r._applyHierarchicalSelection(r.$.mainContainer, e), r._sortPathCollection(e), n = e
                            }
                            break;
                        case "radioButton":
                            { const e = [];r._applyRadioButtonSelection(r.$.mainContainer, n, e), r._sortPathCollection(e), n = e; break }
                    }
                    r.selectedIndexes = n, r._updateState("selected"), r._lastSelectedItem = "one" === a || "oneOrManyExtended" === a ? r._menuItems[n[n.length - 1]] : void 0, r.isRendered && !1 !== arguments[2] && JSON.stringify(t) !== JSON.stringify(n) && r.$.fireEvent("change", { selectedIndexes: r.selectedIndexes, oldSelectedIndexes: t }), r._applyAriaSelected()
                }
                _applyAriaSelected() {
                    const e = this,
                        t = e.selectionMode;
                    for (let r in e._menuItems) {
                        const n = e._menuItems[r];
                        n.selected ? n.setAttribute("aria-selected", !0) : e._canItemBeSelected(n) && -1 !== ["oneOrManyExtended", "zeroOrMany", "oneOrMany", "checkBox", "radioButton"].indexOf(t) ? n.setAttribute("aria-selected", !1) : n.removeAttribute("aria-selected")
                    }
                }
                _autoLoadState(e) {
                    const t = this,
                        r = [];
                    for (let e = 0; e < t._menuItemsGroupsToExpand.length; e++) t._menuItemsGroupsToExpand[e].set("expanded", !1);
                    t._menuItemsGroupsToExpand = [];
                    for (let r = 0; r < e.expanded.length; r++) {
                        const n = t.getItem(e.expanded[r]);
                        n && t._menuItemsGroupsToExpand.push(n)
                    }
                    t.filterable && e.filter && (t._applyFilter(e.filter), t.$.filterInput.value = e.filter);
                    for (let n = 0; n < e.selected.length; n++) {
                        const l = t.getItem(e.selected[n]);
                        l && r.push(l.path)
                    }
                    t.selectedIndexes = r
                }
                _blurHandler() { this._discardKeyboardHover(!0) }
                _canItemBeHovered(e) { const t = e.level; return !1 === e.disabled && !0 !== e.templateApplied && !0 !== e.hidden && (1 === t || t > 1 && this._isContainerOpened(t, e.parentElement.container) && e.getBoundingClientRect().height > 0) }
                _canItemBeSelected(e, t) { return !(!0 !== t && "leaf" === this.selectionTarget && e instanceof Smart.TreeItemsGroup) && !1 === e.disabled && !0 !== e.templateApplied }
                _checkOverflow() {
                    const e = this,
                        t = e.$.scrollViewer,
                        r = e.overflow;
                    if ("scrollbar" === e.scrollMode || "hidden" === r) return void t.refresh();
                    const n = t.scrollTop;
                    "auto" === r && (t.$.removeClass("scroll-buttons-shown"), t.$.removeClass("one-button-shown"), e.$scrollButtonNear.addClass("smart-hidden"), e.$scrollButtonFar.addClass("smart-hidden"));
                    const l = Math.round(t.$.scrollViewerContentContainer.offsetHeight) > Math.round(t.$.scrollViewerContainer.offsetHeight),
                        a = Math.round(t.scrollTop) > 0,
                        o = Math.round(t.$.scrollViewerContainer.offsetHeight + t.scrollTop) < Math.round(t.$.scrollViewerContentContainer.offsetHeight);
                    l ? "auto" === r ? (t.$.addClass("scroll-buttons-shown"), a && e.$scrollButtonNear.removeClass("smart-hidden"), o && e.$scrollButtonFar.removeClass("smart-hidden"), !1 === (a && o) && t.$.addClass("one-button-shown"), e.disabled || (e.$.scrollButtonNear.disabled = !1, e.$.scrollButtonFar.disabled = !1), t.scrollTop = n) : (e.$scrollButtonNear.removeClass("smart-hidden"), e.$scrollButtonFar.removeClass("smart-hidden"), e.disabled ? (e.$.scrollButtonNear.disabled = !0, e.$.scrollButtonFar.disabled = !0) : (e.$.scrollButtonNear.disabled = !a, e.$.scrollButtonFar.disabled = !o)) : "scroll" === r && (e.$.scrollButtonNear.disabled = !0, e.$.scrollButtonFar.disabled = !0), t.refresh()
                }
                _createElement() {
                    const e = this,
                        t = window.getComputedStyle(e.$.scrollViewer);
                    if (e.setAttribute("role", "tree"), e.setAttribute("aria-multiselectable", -1 !== ["oneOrManyExtended", "zeroOrMany", "oneOrMany", "checkBox", "radioButton"].indexOf(e.selectionMode)), e.setAttribute("aria-orientation", "vertical"), e.$.scrollViewer.onVerticalChange = e._verticalScrollbarHandler, e.isRendered || Object.defineProperty(e, "dataSource", { get: function() { return e.context === e ? e.properties.dataSource.value : e._getDataSource() }, set(t) { e.updateProperty(e, e._properties.dataSource, t) } }), e.id || !e.autoLoadState && !e.autoSaveState || (e.warn(e.localize("noId")), e.autoLoadState = !1, e.autoSaveState = !1), e.mode = "tree", e._element = "tree", e._isMobile = Smart.Utilities.Core.isMobile, e._edgeMacFF = !1, e._autoScrollCoefficient = Smart.Utilities.Core.Browser.Firefox ? 4 : Smart.Utilities.Core.Browser.Edge ? 8 : 2, e._scrollViewerPadding = parseFloat(t.paddingTop) + parseFloat(t.paddingBottom) || 0, e._state = { expanded: [], filter: "", selected: [] }, e._dblclickObject = { numberOfClicks: 0 }, e.autoHideToggleElement && e.$mainContainer.addClass("hidden-arrows"), e.disabled && (e.$.scrollButtonNear.disabled = !0, e.$.scrollButtonFar.disabled = !0), "scrollbar" === e.scrollMode && "scroll" === e.overflow && (e.$.scrollViewer.verticalScrollBarVisibility = "visible"), null === e.dataSource && e.$.mainContainer.firstElementChild instanceof HTMLUListElement && e._processUList(), e.isRendered) return e._menuItems = {}, void(null === e.dataSource ? e._processHTML(e.$.mainContainer, 1) : e._processDataSource());
                    const r = (e.shadowRoot || e).querySelectorAll("smart-tree-item, smart-tree-items-group"),
                        n = function() {
                            let t;
                            e.autoLoadState && (t = window.localStorage.getItem("smartTree" + e.id), t && (t = JSON.parse(t), e.sorted = t.sorted)), e._setFocusable(), e._menuItems = {}, null === e.dataSource ? e._processHTML(e.$.mainContainer, 1) : e._processDataSource(), "scrollButtons" !== e.scrollMode && "hidden" !== e.overflow || e.$.scrollViewer.$.verticalScrollBar.setAttribute("aria-hidden", !0), "scrollButtons" === e.scrollMode && "scroll" === e.overflow && (e.$scrollViewer.addClass("scroll-buttons-shown"), e.$scrollButtonNear.removeClass("smart-hidden"), e.$scrollButtonFar.removeClass("smart-hidden"), e._updateScrollButtonVisibility()), e._checkOverflow(), t && e._autoLoadState(t), e._expandItemsByDefault(), e._applySelection(!0), e._updateState("sorted", e.sorted), e.displayLoadingIndicator && e.$loadingIndicatorContainer.removeClass("smart-hidden"), "center" !== e.loadingIndicatorPosition && e.$loadingIndicatorPlaceHolder.removeClass("smart-hidden"), e.__onCompleted && (e._onCompleted = e.__onCompleted, e.__onCompleted = null, e._onCompleted())
                        };
                    0 === r.length || e.enableShadowDOM || e.isInShadowDOM ? n() : (e._onCompleted && (e.__onCompleted = e._onCompleted, e._onCompleted = null), e._ensureItemsReady(r, n))
                }
                appendChild(e) {
                    const t = this;
                    if (!t.isCompleted) { const e = Array.prototype.slice.call(arguments, 2); return HTMLElement.prototype.appendChild.apply(t, e.concat(Array.prototype.slice.call(arguments))) }
                    t.$.mainContainer && t.$.mainContainer.appendChild(e)
                }
                _dblclickHandler(e, t, r) { "dblclick" !== this.toggleMode || e instanceof Smart.TreeItem || t || this._menuItemsGroupSelectionHandler(e, r) }
                _discardKeyboardHover(e, t) { const r = this;!t && r._hoveredViaKeyboard && (!e && r._hoveredViaKeyboard instanceof Smart.MenuItemsGroup && r._isContainerOpened(r._hoveredViaKeyboard.level + 1, r._hoveredViaKeyboard.container) || (r._hoveredViaKeyboard.removeAttribute("focus"), r._hoveredViaKeyboard = void 0)) }
                _documentUpHandler(e) {
                    if ("pointercancel" === e.originalEvent.type) return;
                    const t = this,
                        r = t._downTimeoutInfo,
                        n = t._dragDetails;
                    !r || n && n.FeedbackShown || (clearTimeout(r.timeout), t.$.scrollViewer.scrollTop !== r.scrollTop && t.getBoundingClientRect().top === r.top || t._continueSelection(r.target, r.event)), delete t._downTimeoutInfo;
                    const l = t._downItem,
                        a = t.isInShadowDOM ? e.originalEvent.composedPath()[0] : e.originalEvent.target;
                    if (delete t._downItem, t._editedItem && !t._editInputDown && (!t._isMobile && a !== t.$.editInput || t._isMobile && t.getRootNode().elementFromPoint(e.clientX, e.clientY) !== t.$.editInput)) return void t._endEditing();
                    if (delete t._editInputDown, l) { const r = a.closest("smart-tree-item") || a.closest("smart-tree-items-group");!r || !r.selected || r !== l || t._dragDetails && t._dragDetails.FeedbackShown || r instanceof Smart.TreeItemsGroup && (a.closest(".smart-tree-items-group-arrow") || a === r.container || a === r.container.firstElementChild) || t._handleSelection(r, e) }
                    if (!n) return;
                    const o = Smart.Tree.hoveredTree,
                        s = Smart.Tree.hoveredItem;
                    if (delete t._dragDetails, delete Smart.Tree.treeItemDragged, delete Smart.Tree.hoveredTree, delete Smart.Tree.hoveredItem, t.$.scrollViewer._scrollView.disableSwipeScroll = !1, !n.FeedbackShown) return;
                    const i = o || t.getRootNode().elementFromPoint(e.clientX, e.clientY);
                    let d;
                    document.body.classList.remove("smart-dragging"), document.body.removeChild(n.Feedback), o && clearInterval(o._dragInterval);
                    const c = n.Item,
                        m = n.Items,
                        u = n.ValidItems;
                    if (!i) return;
                    if (!s || c.contains(s)) return void t.$.fireEvent("dragEnd", { item: c, items: m, target: i, data: n, previousContainer: t, container: o || i, originalEvent: e });
                    if (!o || !o.allowDrop || o.disabled) return;
                    const p = [o];
                    let h;
                    if (s.classList.remove("drop-target"), s.classList.contains("top") ? (s.classList.remove("top"), h = "top", d = 0) : s.classList.contains("bottom") ? (s.classList.remove("bottom"), h = "bottom", d = 2) : (h = "inside", d = 1), n.DropDetails = { item: s, position: h }, o !== t) p.push(t);
                    else if (n.ValidateOnDrop)
                        for (let e = 0; e < u.length; e++)
                            if (u[e].contains(s)) return;
                    if (!t.$.fireEvent("dragEnd", { item: c, items: m, target: s, data: n, previousContainer: t, container: o, originalEvent: e }).defaultPrevented) {
                        o.sorted && o.autoSort && o._unsortItems(o.$.mainContainer);
                        for (let e = 0; e < u.length; e++) t._moveTreeItem(u[e], s, d, p);
                        o.sorted && o.autoSort && o._applyGrouping(o.$.mainContainer), o !== t && o._state.filter && o._applyFilter(o._state.filter)
                    }
                }
                _editInputBlurHandler() { this._endEditing() }
                _endEditing(e) {
                    const t = this,
                        r = t._editedItem;
                    if (!r) return;
                    if (delete t._editedItem, t.$editInput.addClass("smart-hidden"), t.focus(), e) return;
                    const n = t.$.editInput.value,
                        l = t.sorted && t.autoSort,
                        a = t._state.filter;
                    n !== r.label && (r.set("label", n), r.setAttribute("aria-label", n), r.firstElementChild.firstElementChild.firstElementChild.innerHTML = n, l && (t._unsortItems(t.$.mainContainer), t._applyGrouping(t.$.mainContainer)), a && t._applyFilter(a))
                }
                _ensureVisible(e) {
                    const t = this;
                    t._ensureVisibleTreeMode(e, e.getBoundingClientRect(), t.$.scrollViewer, t.$.scrollViewer.getBoundingClientRect(), t._scrollViewerPadding), t._ensureVisibleCallback && t._ensureVisibleCallback(e)
                }
                _pointeroverHandler(e) {
                    const t = (this.isInShadowDOM ? e.composedPath()[0] : e.target).closest(".smart-tree-item-label-element>span");
                    if (!t) return;
                    const r = this.$.container.querySelector(".tooltip");
                    r && (r.classList.remove("tooltip"), r.removeAttribute("title")), t.scrollWidth > t.offsetWidth && (t.classList.add("tooltip"), t.title = t.innerText)
                }
                _filterInputKeydownHandler(e) {
                    if ("PageDown" !== e.key) return void("PageUp" === e.key && (e.preventDefault(), e.stopPropagation()));
                    const t = this;
                    let r;
                    if (e.preventDefault(), e.stopPropagation(), t.selectedIndexes.length > 0) {
                        const e = t.selectedIndexes.slice(0);
                        r = t._lastSelectedItem || t._menuItems[t.selectedIndexes[t.selectedIndexes.length - 1]], "checkBox" !== t.selectionMode && "radioButton" !== t.selectionMode && (t.selectedIndexes = [r.path], t._applySelection(!1, e)), t.focus()
                    } else r = t._getFirstEnabledChild(t.$.mainContainer), t.focus(), r && t._hoverViaKeyboard(r);
                    t._ensureVisible(r)
                }
                _focusHandler() {
                    const e = this;
                    e.selectedIndexes.length > 0 && !e._hoveredViaKeyboard && (e._lastSelectedItem ? e._hoverViaKeyboard(e._lastSelectedItem, !1, void 0, !1) : e._hoverViaKeyboard(e._menuItems[e.selectedIndexes[e.selectedIndexes.length - 1]], !1, void 0, !1))
                }
                _getDataSource() {
                    const e = [];
                    return function e(t, r) {
                        for (let n = 0; n < t.length; n++) {
                            const l = t[n],
                                a = { label: l.label };
                            l.disabled && (a.disabled = !0), l.selected && (a.selected = !0), l.separator && (a.separator = !0), null !== l.value && (a.value = l.value), l instanceof Smart.TreeItem ? l.shortcut && (a.shortcut = l.shortcut) : (l.expanded && (a.expanded = !0), a.items = [], e(l.itemContainer.children, a.items)), r.push(a)
                        }
                    }(this.$.mainContainer.children, e), e
                }
                _handleHierarchicalSelection(e, t) {
                    const r = this;
                    let n = e;
                    for (e.selected ? (e.set("selected", !1), e.setAttribute("aria-selected", !1)) : (e.set("selected", !0), e.setAttribute("aria-selected", !0), e.removeAttribute("indeterminate")); n.parentItem;) {
                        const e = n.parentItem,
                            t = e.itemContainer.children;
                        let l = 0,
                            a = 0;
                        for (let e = 0; e < t.length; e++) t[e].selected ? l++ : t[e].hasAttribute("indeterminate") && a++;
                        r._setThreeStateCheckbox(e, l, a), n = e
                    }
                    e instanceof Smart.TreeItemsGroup && function e(t, r) {
                        const n = t.itemContainer.children;
                        for (let t = 0; t < n.length; t++) {
                            const l = n[t];
                            l.set("selected", r), l.setAttribute("aria-selected", r), l.removeAttribute("indeterminate"), l instanceof Smart.TreeItemsGroup && e(l, r)
                        }
                    }(e, e.selected), t.length = 0;
                    const l = Array.from((r.enableShadowDOM ? r.shadowRoot : r).querySelectorAll("[selected]"));
                    for (let e = 0; e < l.length; e++) t.push(l[e].path);
                    r._sortPathCollection(t)
                }
                _handleSelection(e, t) {
                    const r = this,
                        n = r.selectionMode;
                    if ("none" === n || "programmatic" !== t.type && !r._canItemBeSelected(e)) return;
                    const l = e.selected;
                    if (l && "down" === t.type) return;
                    const a = r.selectedIndexes.slice(0);
                    let o = a.slice(0);
                    switch (n) {
                        case "one":
                        case "zeroAndOne":
                            if (l) return;
                            r._menuItems[o[0]] && (r._menuItems[o[0]].set("selected", !1), r._menuItems[o[0]].removeAttribute("aria-selected")), r.selectedIndexes = [e.path], e.set("selected", !0), e.setAttribute("aria-selected", !0), r._lastSelectedItem = e;
                            break;
                        case "zeroOrOne":
                            l ? (r.selectedIndexes = [], e.set("selected", !1), e.removeAttribute("aria-selected")) : (void 0 !== o[0] && (r._menuItems[o[0]].set("selected", !1), r._menuItems[o[0]].removeAttribute("aria-selected")), r.selectedIndexes = [e.path], e.set("selected", !0), e.setAttribute("aria-selected", !0));
                            break;
                        case "oneOrMany":
                        case "zeroOrMany":
                            if (l) {
                                if (1 === o.length && "zeroOrMany" !== n) return;
                                o.splice(o.indexOf(e.path), 1), e.set("selected", !1), e.setAttribute("aria-selected", !1)
                            } else o.push(e.path), r._sortPathCollection(o), e.set("selected", !0), e.setAttribute("aria-selected", !0);
                            r.selectedIndexes = o;
                            break;
                        case "oneOrManyExtended":
                            {
                                const n = t.ctrlKey || t.metaKey,
                                    l = t.shiftKey;
                                if (!n && !l || l && e === r._lastSelectedItem) {
                                    for (let e = 0; e < o.length; e++) r._menuItems[o[e]].set("selected", !1), r._menuItems[o[e]].setAttribute("aria-selected", !1);
                                    o = [e.path], e.set("selected", !0), e.setAttribute("aria-selected", !0), r._lastSelectedItem = e
                                } else if (n) e.selected && o.length > 1 ? (o.splice(o.indexOf(e.path), 1), e.set("selected", !1), e.setAttribute("aria-selected", !1)) : e.selected || (o.push(e.path), r._sortPathCollection(o), e.set("selected", !0), e.setAttribute("aria-selected", !0), r._lastSelectedItem = e);
                                else if (l) {
                                    for (let e = 0; e < o.length; e++) r._menuItems[o[e]].set("selected", !1), r._menuItems[o[e]].setAttribute("aria-selected", !1);
                                    o = r._selectItemRange(r._lastSelectedItem, e)
                                }
                                r.selectedIndexes = o;
                                break
                            }
                        case "checkBox":
                            r.hasThreeStates ? r._handleHierarchicalSelection(e, o) : l ? (o.splice(o.indexOf(e.path), 1), e.set("selected", !1), e.setAttribute("aria-selected", !1)) : (o.push(e.path), r._sortPathCollection(o), e.set("selected", !0), e.setAttribute("aria-selected", !0)), r.selectedIndexes = o;
                            break;
                        case "radioButton":
                            { if (e.selected) return; let t; for (let r = 0; r < e.parentElement.children.length; r++) { const n = e.parentElement.children[r]; if (n.selected) { t = n; break } } const n = o.indexOf(t.path);t.set("selected", !1), e.setAttribute("aria-selected", !1), e.set("selected", !0), e.setAttribute("aria-selected", !0), o.splice(n, 1), o.push(e.path), r._sortPathCollection(o), r.selectedIndexes = o; break }
                    }
                    if (r._discardKeyboardHover(!0), r._hoverViaKeyboard(e, !1, void 0, !r._treeAnimationInProgress), r._updateState("selected"), JSON.stringify(a) !== JSON.stringify(r.selectedIndexes)) {
                        if (r.ownerElement && !r.ownerElement.isRendered) return;
                        r.$.fireEvent("change", { item: e, selectedIndexes: r.selectedIndexes, oldSelectedIndexes: a })
                    }
                }
                _hoverViaKeyboard(e, t, r, n) {
                    if (!e) return;
                    const l = this;
                    e.setAttribute("focus", ""), l._hoveredViaKeyboard = e, !1 !== n && l._ensureVisible(e), t && l._handleSelection(e, r), l._hoverViaKeyboardCallback && l._hoverViaKeyboardCallback(e)
                }
                _keydownHandler(e) {
                    const t = this,
                        r = e.key;
                    if (t._editedItem) return void("Enter" === r ? t._endEditing() : "Escape" === r && t._endEditing(!0));
                    if (t.getRootNode().activeElement !== t || -1 === ["ArrowDown", "ArrowLeft", "ArrowRight", "ArrowUp", "End", "Enter", "F2", "Home", "PageDown", "PageUp", " "].indexOf(r) || t.disabled || t.displayLoadingIndicator) return;
                    "Enter" !== r && e.preventDefault();
                    const n = Array.from(t.$.mainContainer.querySelectorAll("smart-tree-item, smart-tree-items-group")),
                        l = "one" === t.selectionMode || "oneOrManyExtended" === t.selectionMode && !e.ctrlKey && !e.metaKey,
                        a = t.$.mainContainer.querySelector("[focus]");

                    function o(r) {
                        for (let o = r; o < n.length; o++) {
                            const r = n[o];
                            if (t._canItemBeHovered(r)) {
                                if (a) {
                                    if (a === r) break;
                                    a.removeAttribute("focus")
                                }
                                t._hoverViaKeyboard(r, l, e);
                                break
                            }
                        }
                    }

                    function s(r) {
                        for (let o = r; o >= 0; o--) {
                            const r = n[o];
                            if (t._canItemBeHovered(r)) {
                                if (a) {
                                    if (a === r) break;
                                    a.removeAttribute("focus")
                                }
                                t._hoverViaKeyboard(r, l, e);
                                break
                            }
                        }
                    }

                    function i() { a.level > 1 && t._canItemBeSelected(a.parentItem) && (a.removeAttribute("focus"), t._hoverViaKeyboard(a.parentItem, l, e)) }
                    let d;
                    switch (r) {
                        case "ArrowDown":
                            d = a ? n.indexOf(a) + 1 : 0, o(d);
                            break;
                        case "ArrowLeft":
                            if (!a) return;
                            if (a instanceof Smart.TreeItem) i();
                            else {
                                if (t._isContainerOpened(a.level + 1, a.container)) return void t._closeSubContainersTreeMode(a.level + 1, a.container, !0, !0);
                                i()
                            }
                            break;
                        case "ArrowRight":
                            if (!a || a instanceof Smart.TreeItem) return;
                            if (t._isContainerOpened(a.level + 1, a.container)) {
                                const r = t._getFirstEnabledChild(a.itemContainer);
                                r && (a.removeAttribute("focus"), t._hoverViaKeyboard(r, l, e))
                            } else t._menuItemsGroupSelectionHandler(a, { target: a, type: "keydown" });
                            break;
                        case "ArrowUp":
                            d = a ? n.indexOf(a) - 1 : n.length - 1, s(d);
                            break;
                        case "End":
                            s(n.length - 1);
                            break;
                        case "Enter":
                            a && a instanceof Smart.TreeItemsGroup && t._menuItemsGroupSelectionHandler(a, { target: a, type: "keydown" });
                            break;
                        case "F2":
                            t.editable && t._startEditing(a);
                            break;
                        case "Home":
                            o(0);
                            break;
                        case "PageDown":
                            t._pageDownHandler(n, a, l, e);
                            break;
                        case "PageUp":
                            t._pageUpHandler(n, a, l, e);
                            break;
                        case " ":
                            a && t._handleSelection(a, e)
                    }
                }
                _mainContainerSwipeHandler(e) { Smart.Tree.treeItemDragged && e.stopPropagation() }
                _menuItemsGroupSelectionHandler(e, t, r) {
                    const n = this,
                        l = n.toggleMode,
                        a = !!t.originalEvent && t.originalEvent.target.classList.contains("smart-tree-items-group-arrow"),
                        o = e.container;
                    if (n._waitAnimation && n._treeAnimationInProgress) return;
                    if ("down" !== t.type || a || "dblclick" === l && 1 !== n._dblclickObject.numberOfClicks || n._handleSelection(e, t), "down" === t.type && !a && ("dblclick" === l && 2 !== n._dblclickObject.numberOfClicks || "click" === l && n._dblclickObject.numberOfClicks > 1 || "arrow" === l) || e.hiddenChildren) return;
                    const s = o.level;
                    let i = n.hasAnimation;
                    if ("keydown" === t.type && n._discardKeyboardHover(), n._treeAnimationInProgress && (o.removeEventListener("transitionend", n._transitionendHandlerExpand), o.removeEventListener("transitionend", n._transitionendHandlerCollapse)), n._isContainerOpened(s, o)) n._closeSubContainersTreeMode(s, o, !0, !1 !== r);
                    else {
                        if (n.$.fireEvent("expanding", { item: e, label: e.label, path: e.path, value: e.value, children: e.itemContainer.children }).defaultPrevented) return;
                        if (n._handleSingleExpandMode(e), i && ("expand" !== t.type && (n._ensureVisibleOnTransitionend = e), n._expandSection(o)), o.$.removeClass("smart-visibility-hidden"), "keydown" === t.type && (e.setAttribute("focus", ""), n._hoveredViaKeyboard = e), e.$.addClass("smart-tree-items-group-opened"), e.$.addClass("smart-tree-items-group-expanded"), n._addOpenedContainer(s, o), void 0 === t.type && n._hoverViaKeyboard(n._getFirstEnabledChild(e.itemContainer)), !1 !== r) {
                            const t = { item: e, label: e.label, path: e.path, value: e.value, children: e.itemContainer.children };
                            n.toggleCallback ? (t.type = "expand", n.toggleCallback(t)) : n.$.fireEvent("expand", t)
                        }
                    }
                    i || (n._checkOverflow(), "expand" !== t.type && n._ensureVisible(e))
                }
                _handleSingleExpandMode(e) {
                    const t = this;
                    if ("single" !== t.expandMode) return;
                    const r = e.parentItem,
                        n = t._state.expanded.map((e => Object.values(t._menuItems).find((t => t.id === e)))).filter((e => e.parentItem === r));
                    n.length > 0 && n.forEach((e => t.collapseItem(e)))
                }
                _mouseenterHandler() {
                    const e = this;
                    e.autoHideToggleElement && e.$mainContainer.removeClass("hidden-arrows"), Smart.Tree.treeItemDragged && e.allowDrop && !e.disabled && (Smart.Tree.hoveredTree = e)
                }
                _mouseleaveHandler() {
                    const e = this;
                    if (e.autoHideToggleElement && e.$mainContainer.addClass("hidden-arrows"), Smart.Tree.treeItemDragged) {
                        Smart.Tree.hoveredTree && (clearInterval(Smart.Tree.hoveredTree._dragInterval), delete Smart.Tree.hoveredTree);
                        const e = Smart.Tree.hoveredItem;
                        e && (e.classList.remove("drop-target"), e.classList.remove("top"), e.classList.remove("bottom"), delete Smart.Tree.hoveredItem)
                    }
                }
                _moveHandler(e) {
                    const t = this,
                        r = t._dragDetails;
                    if (!r) return;
                    if (!r.FeedbackShown) {
                        if (!(Math.abs(r.StartPosition.left - e.pageX) > 5 || Math.abs(r.StartPosition.top - e.pageY) > 5)) return;
                        if (t.$.fireEvent("dragStart", { item: r.Item, items: r.Items, data: r, container: t, previousContainer: t, originalEvent: r.OriginalEvent }).defaultPrevented) return delete t._dragDetails, delete Smart.Tree.treeItemDragged, delete Smart.Tree.hoveredTree, delete Smart.Tree.hoveredItem, void(t.$.scrollViewer._scrollView.disableSwipeScroll = !1);
                        document.body.classList.add("smart-dragging"), r.Feedback = t._addDragFeedback(), r.FeedbackShown = !0
                    }
                    const n = t.dragOffset;
                    let l, a, o;
                    if (t.$.fireEvent("dragging", { item: r.Item, items: r.Items, data: r, originalEvent: e }), r.Feedback.style.left = e.pageX + n[0] + "px", r.Feedback.style.top = e.pageY + n[1] + "px", t._isMobile) {
                        const r = Smart.Tree.hoveredItem;
                        r && (r.classList.remove("drop-target"), r.classList.remove("top"), r.classList.remove("bottom"), delete Smart.Tree.hoveredItem);
                        const n = t.getRootNode().elementFromPoint(e.clientX, e.clientY);
                        Smart.Tree.hoveredTree && (clearInterval(Smart.Tree.hoveredTree._dragInterval), delete Smart.Tree.hoveredTree), n && (l = n.closest("smart-tree"), l && l.allowDrop && (Smart.Tree.hoveredTree = l, a = n.closest("smart-tree-item") || n.closest("smart-tree-items-group"), a ? o = a : a = n))
                    }
                    if (l = Smart.Tree.hoveredTree, !l) return;
                    const s = l.filterable ? l.$.filterInput.offsetHeight + 10 : 0;
                    if (clearInterval(l._dragInterval), l._dragInterval = setInterval((function() {
                            const r = l.getBoundingClientRect();
                            l.$.scrollViewer.scrollHeight > 0 && r.left <= e.clientX && r.left + r.width >= e.clientX ? e.clientY >= r.top + s && e.clientY <= r.top + 20 + s ? (l.$.scrollViewer.scrollTop -= t._autoScrollCoefficient, "scrollButtons" === l.scrollMode && l._updateScrollButtonVisibility()) : e.clientY >= r.top + r.height - 20 && e.clientY <= r.top + r.height ? (l.$.scrollViewer.scrollTop += t._autoScrollCoefficient, "scrollButtons" === l.scrollMode && l._updateScrollButtonVisibility()) : clearInterval(l._dragInterval) : clearInterval(l._dragInterval)
                        }), 1), t._isMobile || (a = e.originalEvent.target, a && a.enableShadowDOM && (a = e.originalEvent.composedPath()[0]), a && a.closest && (o = a.closest("smart-tree-item") || a.closest("smart-tree-items-group"))), o) {
                        if (Smart.Tree.hoveredItem && o !== Smart.Tree.hoveredItem && (Smart.Tree.hoveredItem.classList.remove("drop-target"), Smart.Tree.hoveredItem.classList.remove("top"), Smart.Tree.hoveredItem.classList.remove("bottom")), Smart.Tree.hoveredItem = o, r.Item.contains(o)) return;
                        const t = o.getBoundingClientRect();
                        o instanceof Smart.TreeItem ? e.clientY - t.top <= t.height / 2 ? (o.classList.remove("bottom"), o.classList.add("top")) : (o.classList.remove("top"), o.classList.add("bottom")) : e.clientY - t.top <= 10 ? (o.classList.remove("bottom"), o.classList.add("top")) : !o.expanded && t.bottom - e.clientY <= 10 ? (o.classList.remove("top"), o.classList.add("bottom")) : (o.classList.remove("top"), o.classList.remove("bottom")), o.classList.add("drop-target")
                    } else if (Smart.Tree.hoveredItem && (Smart.Tree.hoveredItem.classList.remove("drop-target"), Smart.Tree.hoveredItem.classList.remove("top"), Smart.Tree.hoveredItem.classList.remove("bottom")), a === l.$.scrollViewer.$.scrollViewerContainer)
                        if (l._menuItems[0]) {
                            let e = l.$.mainContainer.lastElementChild,
                                t = l.$.mainContainer.childElementCount - 1;
                            for (; e.hidden && (t--, e = l.$.mainContainer.children[t], e););
                            if (e) {
                                if (r.Item === e) return;
                                Smart.Tree.hoveredItem = e, Smart.Tree.hoveredItem.classList.add("bottom")
                            } else Smart.Tree.hoveredItem = l.$.container;
                            Smart.Tree.hoveredItem.classList.add("drop-target")
                        } else Smart.Tree.hoveredItem = l.$.container, Smart.Tree.hoveredItem.classList.add("drop-target");
                    else delete Smart.Tree.hoveredItem
                }
                _moveSubItems(e, t, r) {
                    const n = this;
                    for (let l = 0; l < e.length; l++) {
                        const a = e[l];
                        a.menu = t, a.set("level", a.parentItem.level + 1), a.firstElementChild.style.paddingLeft = "", a.firstElementChild.style.paddingRight = "", n._setIndentation(a.firstElementChild, a.level, r), a.hidden = !1, a.$.removeClass("smart-hidden"), a.$.removeClass("filtered-child"), a.$.removeClass("last-filtered-child"), a instanceof Smart.TreeItemsGroup && (a.$.removeClass("hidden-children"), a.container.level = a.level + 1, n._moveSubItems(a.itemContainer.children, t, r), t !== n && a.expanded && (t._menuItemsGroupsToExpand.push(a), n._updateState("expanded", a.id, !1)))
                    }
                }
                _moveTreeItem(e, t, r, n) {
                    const l = this,
                        a = e.level;
                    if (0 === r) {
                        if (t.previousElementSibling === e) return;
                        t.parentElement.insertBefore(e, t), e.set("level", t.level), e.parentItem = t.parentItem
                    } else if (2 === r) {
                        if (t.nextElementSibling === e) return;
                        t.parentElement.insertBefore(e, t.nextElementSibling || null), e.set("level", t.level), e.parentItem = t.parentItem
                    } else if (t === n[0].$.container) n[0].$.mainContainer.appendChild(e), e.set("level", 1), e.parentItem = void 0;
                    else {
                        if (t.itemContainer.lastElementChild === e) return;
                        t.itemContainer.appendChild(e), e.set("level", t.level + 1), e.parentItem = t
                    }
                    const o = n[0].rightToLeft ? "paddingRight" : "paddingLeft";
                    if (e.menu = n[0], e.parentItem = e.parentElement.menuItemsGroup, e.firstElementChild.style.paddingLeft = "", e.firstElementChild.style.paddingRight = "", l._setIndentation(e.firstElementChild, e.level, o), e.hidden = !1, e.$.removeClass("smart-hidden"), e.$.removeClass("filtered-child"), e.$.removeClass("last-filtered-child"), e instanceof Smart.TreeItemsGroup && (e.$.removeClass("hidden-children"), e.container.level = e.level + 1, l._moveSubItems(e.itemContainer.children, n[0], o), e.expanded)) { const t = l._openedContainers[a + 1].indexOf(e.container); - 1 !== t && l._openedContainers[a + 1].splice(t, 1), n[0]._menuItemsGroupsToExpand.push(e), 2 === n.length && l._updateState("expanded", e.id, !1) }
                    for (let e = 0; e < n.length; e++) {
                        const t = n[e],
                            r = t.context,
                            l = t.selectedIndexes.slice(0);
                        t.context = t, t._menuItems = {}, t._refreshItemPaths(t.$.mainContainer, !0, void 0, t.sorted && !t.autoSort), t.selectedIndexes = [], t._applySelection(!0, l, !1), t._checkOverflow(), t.context = r
                    }
                    n[0]._expandItemsByDefault()
                }
                _overriddenMenuHandler() {}
                _pageDownHandler(e, t, r, n) {
                    const l = this,
                        a = l.$.scrollViewer;

                    function o() { for (let t = e.length - 1; t >= 0; t--) { const r = e[t]; if (l._canItemBeHovered(r) && l._getOffsetTop(r) + r.firstElementChild.offsetHeight <= a.scrollTop + a.$.container.offsetHeight) return r } }
                    if (!t) return;
                    let s = o();
                    s && (t !== s ? (t.removeAttribute("focus"), l._hoverViaKeyboard(s, r, n)) : a.scrollTop + a.$.container.offsetHeight !== a.$.scrollViewerContentContainer.offsetHeight && (l.$.scrollViewer.scrollTop += a.$.container.offsetHeight, "scrollButtons" === l.scrollMode && l._updateScrollButtonVisibility(), s = o(), t.removeAttribute("focus"), l._hoverViaKeyboard(s, r, n)))
                }
                _pageUpHandler(e, t, r, n) {
                    const l = this,
                        a = l.$.scrollViewer;

                    function o() { for (let t = 0; t < e.length; t++) { const r = e[t]; if (l._canItemBeHovered(r) && l._getOffsetTop(r) >= a.scrollTop) return r } }
                    if (!t) return;
                    let s = o();
                    s && (t !== s ? (t.removeAttribute("focus"), l._hoverViaKeyboard(s, r, n)) : 0 !== a.scrollTop ? (l.$.scrollViewer.scrollTop -= a.$.container.offsetHeight, "scrollButtons" === l.scrollMode && l._updateScrollButtonVisibility(), s = o(), t.removeAttribute("focus"), l._hoverViaKeyboard(s, r, n)) : l.filterable && l.$.filterInput.focus())
                }
                _refreshItemPathsAndSelection() {
                    const e = this,
                        t = e.selectedIndexes.slice(0);
                    e._menuItems = {}, e._refreshItemPaths(e.$.mainContainer, !0), e.selectedIndexes = [], e._applySelection(!0, t)
                }
                _refreshSorting() {
                    const e = this;
                    e._unsortItems(e.$.mainContainer), e._applyGrouping(e.$.mainContainer);
                    const t = e._state.filter;
                    t && e._applyFilter(t), e._checkOverflow()
                }
                _scroll(e) {
                    const t = this;
                    t.$.scrollViewer.scrollTop = t.$.scrollViewer.scrollTop + 10 * e, t._updateScrollButtonVisibility(), t.focus()
                }
                _scrollButtonFarClickHandler() { this.$.scrollButtonFar.disabled || this._scroll(1) }
                _scrollButtonNearClickHandler() { this.$.scrollButtonNear.disabled || this._scroll(-1) }
                _scrollViewerDownHandler(e) {
                    const t = this;
                    if (e.target !== t.$.scrollViewer || t.disabled || t.displayLoadingIndicator || !t._isMobile && 1 !== e.which) return;
                    const r = e.originalEvent.target;
                    if (r !== t.$.editInput)
                        if (t._isMobile) {
                            const n = t.$.scrollViewer.scrollTop,
                                l = t.getBoundingClientRect().top,
                                a = setTimeout((function() {
                                    if (!t._dragDetails && t.$.scrollViewer.scrollTop === n && t.getBoundingClientRect().top === l) {
                                        const n = t.context;
                                        t.context = t, t._continueSelection(r, e), t.context = n
                                    }
                                }), 250);
                            t._downTimeoutInfo = { target: r, event: e, scrollTop: n, top: l, timeout: a }
                        } else t._continueSelection(r, e);
                    else t._editInputDown = !0
                }
                _continueSelection(e, t) {
                    const r = this,
                        n = e.closest("smart-tree-item") || e.closest("smart-tree-items-group");
                    if (!(n && n.parentElement && r._canItemBeSelected(n, !0))) return;
                    const l = e.closest(".smart-tree-items-group-arrow");
                    let a;
                    if (n instanceof Smart.TreeItem) a = "_handleSelection";
                    else {
                        if (e === n.container || e === n.container.firstElementChild) return;
                        a = "_menuItemsGroupSelectionHandler"
                    }
                    if (clearTimeout(r._dblclickTimeout), n !== r._dblclickObject.target && (r._dblclickObject.numberOfClicks = 0), r._dblclickObject.target = n, r._dblclickObject.numberOfClicks++, r._dblclickTimeout = setTimeout((function() { r._dblclickObject.numberOfClicks = 0 }), 300), 2 === r._dblclickObject.numberOfClicks) {
                        if (r.editable) return void r._startEditing(n);
                        r._dblclickHandler(n, l, t), r._dblclickObject.numberOfClicks = 0
                    }
                    n.selected && (r._downItem = n), r[a](n, t), r._discardKeyboardHover(!0), r._hoverViaKeyboard(n, !1, void 0, !1), l || r._startDragging(n, t)
                }
                _scrollViewerTouchmoveHandler(e) { this._dragDetails && e.cancelable && (e.preventDefault(), e.stopPropagation()) }
                _scrollViewerWheelHandler() { const e = this; "scrollButtons" === e.scrollMode && "hidden" !== e.overflow && e._updateScrollButtonVisibility() }
                _selectItemRange(e, t) {
                    const r = this,
                        n = Array.from(r.$.mainContainer.querySelectorAll("smart-tree-item, smart-tree-items-group")),
                        l = n.indexOf(e),
                        a = n.indexOf(t),
                        o = [];
                    for (let e = Math.min(l, a); e <= Math.max(l, a); e++) {
                        const t = n[e];
                        r._canItemBeHovered(t) && (o.push(t.path), t.set("selected", !0))
                    }
                    return o
                }
                _selectstartHandler(e) { this._dragDetails && e.preventDefault() }
                _setFocusable() {
                    super._setFocusable();
                    const e = this;
                    e.disabled || e.unfocusable ? e.$.filterInput.tabIndex = -1 : e.$.filterInput.removeAttribute("tabindex")
                }
                _setIndentation(e, t, r) {
                    const n = this;
                    let l = n._paddingSize;
                    void 0 === l && (l = parseFloat(getComputedStyle(n).getPropertyValue("--smart-tree-indent")), isNaN(l) ? l = 20 : l += 4, n._paddingSize = l), e.style[r] = t * l - l / 2 + "px"
                }
                _setThreeStateCheckbox(e, t, r) { t === e.itemContainer.childElementCount && t > 0 ? (e.removeAttribute("indeterminate"), e.set("selected", !0), e.setAttribute("aria-selected", !0)) : 0 === t && 0 === r ? (e.removeAttribute("indeterminate"), e.set("selected", !1), e.setAttribute("aria-selected", !1)) : (e.setAttribute("indeterminate", ""), e.set("selected", !1), e.setAttribute("aria-selected", !1)) }
                _sortItems(e) {
                    const t = this;
                    if (!t.sorted) return;
                    let r;
                    e instanceof Smart.TreeItemsGroup ? r = e.container.firstElementChild : e === t.$.mainContainer && (r = e);
                    let n = Array.from(r.children);
                    if (t.sort) {
                        const r = t.sort(n, e);
                        Array.isArray(r) && (n = r)
                    } else "asc" === t.sortDirection ? n.sort((function(e, t) { return e.label.localeCompare(t.label) })) : n.sort((function(e, t) { return t.label.localeCompare(e.label) }));
                    for (let e = n.length - 1; e >= 0; e--) r.insertBefore(n[e], r.firstElementChild)
                }
                _sortPathCollection(e) {
                    e.sort((function(e, t) {
                        const r = e.split("."),
                            n = t.split("."),
                            l = Math.max(r.length, n.length);
                        for (let e = 0; e < l; e++) {
                            const t = parseFloat(r[e]),
                                l = parseFloat(n[e]);
                            if (isNaN(t)) return -1;
                            if (isNaN(l)) return 1;
                            if (t < l) return -1;
                            if (t > l) return 1
                        }
                    }))
                }
                _startDragging(e, t) {
                    const r = this,
                        n = r.selectionMode;
                    if (!r.allowDrag || r._editedItem || "none" === n) return;
                    const l = [],
                        a = [];
                    let o;
                    if (-1 !== ["one", "zeroAndOne", "zeroOrOne", "checkBox", "radioButton"].indexOf(n)) o = !1, l.push(e), a.push(e);
                    else {
                        o = !0;
                        for (let e = 0; e < r.selectedIndexes.length; e++) l.push(r._menuItems[r.selectedIndexes[e]]), a.push(l[e]);
                        for (let e = 0; e < l.length; e++) {
                            const t = l[e];
                            if (-1 !== a.indexOf(t))
                                for (let e = a.length - 1; e >= 0; e--) {
                                    const r = a[e];
                                    if (r === t) break;
                                    t.contains(r) && a.splice(e, 1)
                                }
                        }
                    }
                    r._dragDetails = { StartPosition: { left: t.pageX, top: t.pageY }, Items: l, ValidItems: a, Item: e, FeedbackShown: !1, ValidateOnDrop: o, OriginalEvent: t, StartTime: new Date, Dragging: !0 }, Smart.Tree.treeItemDragged = !0, r.$.scrollViewer._scrollView.disableSwipeScroll = !0, r.allowDrop && (Smart.Tree.hoveredTree = r, Smart.Tree.hoveredItem = e)
                }
                _startEditing(e) {
                    const t = this,
                        r = t.$.editInput;
                    let n, l;
                    if (!t._canItemBeSelected(e, !0)) return;
                    const a = e.firstElementChild,
                        o = a.firstElementChild;
                    t.rightToLeft ? (n = function() { return a.offsetWidth - o.offsetLeft - o.offsetWidth }, l = "paddingRight") : (n = function() { return o.offsetLeft + parseFloat(window.getComputedStyle(a).borderLeftWidth) }, l = "paddingLeft"), e instanceof Smart.TreeItemsGroup ? (r.style[l] = n() + (t.showLines ? parseFloat(window.getComputedStyle(o.firstElementChild).paddingLeft) : 0) - 1 + "px", r.style.height = a.offsetHeight + "px") : (r.style[l] = e.offsetWidth + parseInt(a.style[l], 10) - a.offsetWidth + parseFloat(window.getComputedStyle(o.firstElementChild).paddingLeft) - 2 + "px", r.style.height = e.offsetHeight + "px"), r.style.top = t._getOffsetTop(e) + "px", t.$editInput.removeClass("smart-hidden"), r.value = e.label, t._editedItem = e, r.setAttribute("aria-label", "Edit item " + e.label), setTimeout((function() { r.focus() }), 0)
                }
                _styleChangedHandler(e) { e.detail.styleProperties && e.detail.styleProperties["font-size"] && this._checkOverflow() }
                _updateScrollButtonVisibility() {
                    const e = this,
                        t = e.overflow;
                    if ("scrollbar" === e.scrollMode || "hidden" === t) return;
                    let r = !0,
                        n = !0;
                    if (0 === Math.round(e.$.scrollViewer.scrollTop) && (r = !1), Math.round(e.$.scrollViewer.$.scrollViewerContainer.offsetHeight + e.$.scrollViewer.scrollTop) >= Math.round(e.$.scrollViewer.$.scrollViewerContentContainer.offsetHeight) && (n = !1), "auto" === t) {
                        if (r && n) return e.$scrollButtonNear.removeClass("smart-hidden"), e.$scrollButtonFar.removeClass("smart-hidden"), e.$scrollViewer.removeClass("one-button-shown"), void e.$.scrollViewer.refresh();
                        r ? e.$scrollButtonNear.removeClass("smart-hidden") : e.$scrollButtonNear.addClass("smart-hidden"), n ? e.$scrollButtonFar.removeClass("smart-hidden") : e.$scrollButtonFar.addClass("smart-hidden"), e.$scrollViewer.addClass("one-button-shown"), e.$.scrollViewer.refresh()
                    } else "scroll" !== t || e.disabled || (e.$.scrollButtonNear.disabled = !r, e.$.scrollButtonFar.disabled = !n)
                }
                _updateState(e, t, r) {
                    const n = this;
                    switch (e) {
                        case "expanded":
                            {
                                const e = n._state.expanded.indexOf(t);
                                if (r && -1 === e) n._state.expanded.push(t);
                                else {
                                    if (r || -1 === e) return;
                                    n._state.expanded.splice(e, 1)
                                }
                                break
                            }
                        case "filter":
                            n._state.filter = void 0 !== t ? t : n.$.filterInput.value;
                            break;
                        case "selected":
                            n._state.selected = [];
                            for (let e = 0; e < n.selectedIndexes.length; e++) {
                                const t = n._menuItems[n.selectedIndexes[e]];
                                n._state.selected.push(t.id)
                            }
                            break;
                        case "sorted":
                            n._state.sorted = t
                    }
                    n.autoSaveState && window.localStorage.setItem("smartTree" + n.id, JSON.stringify(n._state))
                }
                _verticalScrollbarHandler() {
                    const e = this,
                        t = e.$.verticalScrollBar,
                        r = t.value;
                    e.disabled || (t.max !== r ? t.min !== r ? (delete e._topReached, delete e._bottomReached) : e._topReached || (e.$.fireEvent("scrollTopReached"), delete e._bottomReached, e._topReached = !0) : e._bottomReached || (e.$.fireEvent("scrollBottomReached"), delete e._topReached, e._bottomReached = !0))
                }
            });

            /***/
        })

        /******/
    });
    /************************************************************************/
    /******/ // The module cache
    /******/
    var __webpack_module_cache__ = {};
    /******/
    /******/ // The require function
    /******/
    function __webpack_require__(moduleId) {
        /******/ // Check if module is in cache
        /******/
        var cachedModule = __webpack_module_cache__[moduleId];
        /******/
        if (cachedModule !== undefined) {
            /******/
            return cachedModule.exports;
            /******/
        }
        /******/ // Create a new module (and put it into the cache)
        /******/
        var module = __webpack_module_cache__[moduleId] = {
            /******/ // no module.id needed
            /******/ // no module.loaded needed
            /******/
            exports: {}
            /******/
        };
        /******/
        /******/ // Execute the module function
        /******/
        __webpack_modules__[moduleId](module, module.exports, __webpack_require__);
        /******/
        /******/ // Return the exports of the module
        /******/
        return module.exports;
        /******/
    }
    /******/
    /************************************************************************/
    /******/
    /* webpack/runtime/compat get default export */
    /******/
    (() => {
        /******/ // getDefaultExport function for compatibility with non-harmony modules
        /******/
        __webpack_require__.n = (module) => {
            /******/
            var getter = module && module.__esModule ?
                /******/
                () => (module['default']) :
                /******/
                () => (module);
            /******/
            __webpack_require__.d(getter, { a: getter });
            /******/
            return getter;
            /******/
        };
        /******/
    })();
    /******/
    /******/
    /* webpack/runtime/define property getters */
    /******/
    (() => {
        /******/ // define getter functions for harmony exports
        /******/
        __webpack_require__.d = (exports, definition) => {
            /******/
            for (var key in definition) {
                /******/
                if (__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
                    /******/
                    Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
                    /******/
                }
                /******/
            }
            /******/
        };
        /******/
    })();
    /******/
    /******/
    /* webpack/runtime/hasOwnProperty shorthand */
    /******/
    (() => {
        /******/
        __webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
            /******/
    })();
    /******/
    /************************************************************************/
    var __webpack_exports__ = {};
    // This entry need to be wrapped in an IIFE because it need to be in strict mode.
    (() => {
        "use strict";
        /* unused harmony export smartTree */
        /* harmony import */
        var _smart_element_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(6321);
        /* harmony import */
        var _smart_element_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/ __webpack_require__.n(_smart_element_js__WEBPACK_IMPORTED_MODULE_0__);
        /* harmony import */
        var _smart_button_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(2612);
        /* harmony import */
        var _smart_button_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/ __webpack_require__.n(_smart_button_js__WEBPACK_IMPORTED_MODULE_1__);
        /* harmony import */
        var _smart_radiobutton_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8649);
        /* harmony import */
        var _smart_radiobutton_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/ __webpack_require__.n(_smart_radiobutton_js__WEBPACK_IMPORTED_MODULE_2__);
        /* harmony import */
        var _smart_checkbox_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(9097);
        /* harmony import */
        var _smart_checkbox_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/ __webpack_require__.n(_smart_checkbox_js__WEBPACK_IMPORTED_MODULE_3__);
        /* harmony import */
        var _smart_scrollbar_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(9135);
        /* harmony import */
        var _smart_scrollbar_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/ __webpack_require__.n(_smart_scrollbar_js__WEBPACK_IMPORTED_MODULE_4__);
        /* harmony import */
        var _smart_menu_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(3661);
        /* harmony import */
        var _smart_menu_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/ __webpack_require__.n(_smart_menu_js__WEBPACK_IMPORTED_MODULE_5__);
        /* harmony import */
        var _smart_tree_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(5482);
        /* harmony import */
        var _smart_tree_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/ __webpack_require__.n(_smart_tree_js__WEBPACK_IMPORTED_MODULE_6__);

        /* Smart UI v13.1.26 (2022-04-05) 
        Copyright (c) 2011-2021 jQWidgets. 
        License: https://htmlelements.com/license/ */ //









        class smartTree extends Smart.Component {
            get name() {
                return 'smartTree';
            }
        }
    })();

    /******/
})();