"use strict";(self.webpackChunkextension=self.webpackChunkextension||[]).push([[356],{23356:(e,t,o)=>{o.d(t,{Z:()=>ht});var n=o(63366),r=o(87462),i=o(72791),a=o(63733),s=o(94419),p=o(90183),l=o(12065),c=o(66934),u=o(13967),f=o(31402),d=o(14036),m=o(13208),h=o(6117),v=o(62876),g=o(84913);function b(e){if(null==e)return window;if("[object Window]"!==e.toString()){var t=e.ownerDocument;return t&&t.defaultView||window}return e}function y(e){return e instanceof b(e).Element||e instanceof Element}function w(e){return e instanceof b(e).HTMLElement||e instanceof HTMLElement}function x(e){return"undefined"!==typeof ShadowRoot&&(e instanceof b(e).ShadowRoot||e instanceof ShadowRoot)}var O=Math.max,T=Math.min,P=Math.round;function Z(){var e=navigator.userAgentData;return null!=e&&e.brands&&Array.isArray(e.brands)?e.brands.map((function(e){return e.brand+"/"+e.version})).join(" "):navigator.userAgent}function R(){return!/^((?!chrome|android).)*safari/i.test(Z())}function E(e,t,o){void 0===t&&(t=!1),void 0===o&&(o=!1);var n=e.getBoundingClientRect(),r=1,i=1;t&&w(e)&&(r=e.offsetWidth>0&&P(n.width)/e.offsetWidth||1,i=e.offsetHeight>0&&P(n.height)/e.offsetHeight||1);var a=(y(e)?b(e):window).visualViewport,s=!R()&&o,p=(n.left+(s&&a?a.offsetLeft:0))/r,l=(n.top+(s&&a?a.offsetTop:0))/i,c=n.width/r,u=n.height/i;return{width:c,height:u,top:l,right:p+c,bottom:l+u,left:p,x:p,y:l}}function M(e){var t=b(e);return{scrollLeft:t.pageXOffset,scrollTop:t.pageYOffset}}function j(e){return e?(e.nodeName||"").toLowerCase():null}function k(e){return((y(e)?e.ownerDocument:e.document)||window.document).documentElement}function D(e){return E(k(e)).left+M(e).scrollLeft}function L(e){return b(e).getComputedStyle(e)}function A(e){var t=L(e),o=t.overflow,n=t.overflowX,r=t.overflowY;return/auto|scroll|overlay|hidden/.test(o+r+n)}function S(e,t,o){void 0===o&&(o=!1);var n=w(t),r=w(t)&&function(e){var t=e.getBoundingClientRect(),o=P(t.width)/e.offsetWidth||1,n=P(t.height)/e.offsetHeight||1;return 1!==o||1!==n}(t),i=k(t),a=E(e,r,o),s={scrollLeft:0,scrollTop:0},p={x:0,y:0};return(n||!n&&!o)&&(("body"!==j(t)||A(i))&&(s=function(e){return e!==b(e)&&w(e)?{scrollLeft:(t=e).scrollLeft,scrollTop:t.scrollTop}:M(e);var t}(t)),w(t)?((p=E(t,!0)).x+=t.clientLeft,p.y+=t.clientTop):i&&(p.x=D(i))),{x:a.left+s.scrollLeft-p.x,y:a.top+s.scrollTop-p.y,width:a.width,height:a.height}}function C(e){var t=E(e),o=e.offsetWidth,n=e.offsetHeight;return Math.abs(t.width-o)<=1&&(o=t.width),Math.abs(t.height-n)<=1&&(n=t.height),{x:e.offsetLeft,y:e.offsetTop,width:o,height:n}}function W(e){return"html"===j(e)?e:e.assignedSlot||e.parentNode||(x(e)?e.host:null)||k(e)}function B(e){return["html","body","#document"].indexOf(j(e))>=0?e.ownerDocument.body:w(e)&&A(e)?e:B(W(e))}function H(e,t){var o;void 0===t&&(t=[]);var n=B(e),r=n===(null==(o=e.ownerDocument)?void 0:o.body),i=b(n),a=r?[i].concat(i.visualViewport||[],A(n)?n:[]):n,s=t.concat(a);return r?s:s.concat(H(W(a)))}function N(e){return["table","td","th"].indexOf(j(e))>=0}function F(e){return w(e)&&"fixed"!==L(e).position?e.offsetParent:null}function I(e){for(var t=b(e),o=F(e);o&&N(o)&&"static"===L(o).position;)o=F(o);return o&&("html"===j(o)||"body"===j(o)&&"static"===L(o).position)?t:o||function(e){var t=/firefox/i.test(Z());if(/Trident/i.test(Z())&&w(e)&&"fixed"===L(e).position)return null;var o=W(e);for(x(o)&&(o=o.host);w(o)&&["html","body"].indexOf(j(o))<0;){var n=L(o);if("none"!==n.transform||"none"!==n.perspective||"paint"===n.contain||-1!==["transform","perspective"].indexOf(n.willChange)||t&&"filter"===n.willChange||t&&n.filter&&"none"!==n.filter)return o;o=o.parentNode}return null}(e)||t}var $="top",V="bottom",q="right",U="left",z="auto",X=[$,V,q,U],Y="start",_="end",G="clippingParents",J="viewport",K="popper",Q="reference",ee=X.reduce((function(e,t){return e.concat([t+"-"+Y,t+"-"+_])}),[]),te=[].concat(X,[z]).reduce((function(e,t){return e.concat([t,t+"-"+Y,t+"-"+_])}),[]),oe=["beforeRead","read","afterRead","beforeMain","main","afterMain","beforeWrite","write","afterWrite"];function ne(e){var t=new Map,o=new Set,n=[];function r(e){o.add(e.name),[].concat(e.requires||[],e.requiresIfExists||[]).forEach((function(e){if(!o.has(e)){var n=t.get(e);n&&r(n)}})),n.push(e)}return e.forEach((function(e){t.set(e.name,e)})),e.forEach((function(e){o.has(e.name)||r(e)})),n}function re(e){var t;return function(){return t||(t=new Promise((function(o){Promise.resolve().then((function(){t=void 0,o(e())}))}))),t}}var ie={placement:"bottom",modifiers:[],strategy:"absolute"};function ae(){for(var e=arguments.length,t=new Array(e),o=0;o<e;o++)t[o]=arguments[o];return!t.some((function(e){return!(e&&"function"===typeof e.getBoundingClientRect)}))}function se(e){void 0===e&&(e={});var t=e,o=t.defaultModifiers,n=void 0===o?[]:o,r=t.defaultOptions,i=void 0===r?ie:r;return function(e,t,o){void 0===o&&(o=i);var r={placement:"bottom",orderedModifiers:[],options:Object.assign({},ie,i),modifiersData:{},elements:{reference:e,popper:t},attributes:{},styles:{}},a=[],s=!1,p={state:r,setOptions:function(o){var s="function"===typeof o?o(r.options):o;l(),r.options=Object.assign({},i,r.options,s),r.scrollParents={reference:y(e)?H(e):e.contextElement?H(e.contextElement):[],popper:H(t)};var c=function(e){var t=ne(e);return oe.reduce((function(e,o){return e.concat(t.filter((function(e){return e.phase===o})))}),[])}(function(e){var t=e.reduce((function(e,t){var o=e[t.name];return e[t.name]=o?Object.assign({},o,t,{options:Object.assign({},o.options,t.options),data:Object.assign({},o.data,t.data)}):t,e}),{});return Object.keys(t).map((function(e){return t[e]}))}([].concat(n,r.options.modifiers)));return r.orderedModifiers=c.filter((function(e){return e.enabled})),r.orderedModifiers.forEach((function(e){var t=e.name,o=e.options,n=void 0===o?{}:o,i=e.effect;if("function"===typeof i){var s=i({state:r,name:t,instance:p,options:n}),l=function(){};a.push(s||l)}})),p.update()},forceUpdate:function(){if(!s){var e=r.elements,t=e.reference,o=e.popper;if(ae(t,o)){r.rects={reference:S(t,I(o),"fixed"===r.options.strategy),popper:C(o)},r.reset=!1,r.placement=r.options.placement,r.orderedModifiers.forEach((function(e){return r.modifiersData[e.name]=Object.assign({},e.data)}));for(var n=0;n<r.orderedModifiers.length;n++)if(!0!==r.reset){var i=r.orderedModifiers[n],a=i.fn,l=i.options,c=void 0===l?{}:l,u=i.name;"function"===typeof a&&(r=a({state:r,options:c,name:u,instance:p})||r)}else r.reset=!1,n=-1}}},update:re((function(){return new Promise((function(e){p.forceUpdate(),e(r)}))})),destroy:function(){l(),s=!0}};if(!ae(e,t))return p;function l(){a.forEach((function(e){return e()})),a=[]}return p.setOptions(o).then((function(e){!s&&o.onFirstUpdate&&o.onFirstUpdate(e)})),p}}var pe={passive:!0};function le(e){return e.split("-")[0]}function ce(e){return e.split("-")[1]}function ue(e){return["top","bottom"].indexOf(e)>=0?"x":"y"}function fe(e){var t,o=e.reference,n=e.element,r=e.placement,i=r?le(r):null,a=r?ce(r):null,s=o.x+o.width/2-n.width/2,p=o.y+o.height/2-n.height/2;switch(i){case $:t={x:s,y:o.y-n.height};break;case V:t={x:s,y:o.y+o.height};break;case q:t={x:o.x+o.width,y:p};break;case U:t={x:o.x-n.width,y:p};break;default:t={x:o.x,y:o.y}}var l=i?ue(i):null;if(null!=l){var c="y"===l?"height":"width";switch(a){case Y:t[l]=t[l]-(o[c]/2-n[c]/2);break;case _:t[l]=t[l]+(o[c]/2-n[c]/2)}}return t}var de={top:"auto",right:"auto",bottom:"auto",left:"auto"};function me(e){var t,o=e.popper,n=e.popperRect,r=e.placement,i=e.variation,a=e.offsets,s=e.position,p=e.gpuAcceleration,l=e.adaptive,c=e.roundOffsets,u=e.isFixed,f=a.x,d=void 0===f?0:f,m=a.y,h=void 0===m?0:m,v="function"===typeof c?c({x:d,y:h}):{x:d,y:h};d=v.x,h=v.y;var g=a.hasOwnProperty("x"),y=a.hasOwnProperty("y"),w=U,x=$,O=window;if(l){var T=I(o),Z="clientHeight",R="clientWidth";if(T===b(o)&&"static"!==L(T=k(o)).position&&"absolute"===s&&(Z="scrollHeight",R="scrollWidth"),r===$||(r===U||r===q)&&i===_)x=V,h-=(u&&T===O&&O.visualViewport?O.visualViewport.height:T[Z])-n.height,h*=p?1:-1;if(r===U||(r===$||r===V)&&i===_)w=q,d-=(u&&T===O&&O.visualViewport?O.visualViewport.width:T[R])-n.width,d*=p?1:-1}var E,M=Object.assign({position:s},l&&de),j=!0===c?function(e,t){var o=e.x,n=e.y,r=t.devicePixelRatio||1;return{x:P(o*r)/r||0,y:P(n*r)/r||0}}({x:d,y:h},b(o)):{x:d,y:h};return d=j.x,h=j.y,p?Object.assign({},M,((E={})[x]=y?"0":"",E[w]=g?"0":"",E.transform=(O.devicePixelRatio||1)<=1?"translate("+d+"px, "+h+"px)":"translate3d("+d+"px, "+h+"px, 0)",E)):Object.assign({},M,((t={})[x]=y?h+"px":"",t[w]=g?d+"px":"",t.transform="",t))}const he={name:"offset",enabled:!0,phase:"main",requires:["popperOffsets"],fn:function(e){var t=e.state,o=e.options,n=e.name,r=o.offset,i=void 0===r?[0,0]:r,a=te.reduce((function(e,o){return e[o]=function(e,t,o){var n=le(e),r=[U,$].indexOf(n)>=0?-1:1,i="function"===typeof o?o(Object.assign({},t,{placement:e})):o,a=i[0],s=i[1];return a=a||0,s=(s||0)*r,[U,q].indexOf(n)>=0?{x:s,y:a}:{x:a,y:s}}(o,t.rects,i),e}),{}),s=a[t.placement],p=s.x,l=s.y;null!=t.modifiersData.popperOffsets&&(t.modifiersData.popperOffsets.x+=p,t.modifiersData.popperOffsets.y+=l),t.modifiersData[n]=a}};var ve={left:"right",right:"left",bottom:"top",top:"bottom"};function ge(e){return e.replace(/left|right|bottom|top/g,(function(e){return ve[e]}))}var be={start:"end",end:"start"};function ye(e){return e.replace(/start|end/g,(function(e){return be[e]}))}function we(e,t){var o=t.getRootNode&&t.getRootNode();if(e.contains(t))return!0;if(o&&x(o)){var n=t;do{if(n&&e.isSameNode(n))return!0;n=n.parentNode||n.host}while(n)}return!1}function xe(e){return Object.assign({},e,{left:e.x,top:e.y,right:e.x+e.width,bottom:e.y+e.height})}function Oe(e,t,o){return t===J?xe(function(e,t){var o=b(e),n=k(e),r=o.visualViewport,i=n.clientWidth,a=n.clientHeight,s=0,p=0;if(r){i=r.width,a=r.height;var l=R();(l||!l&&"fixed"===t)&&(s=r.offsetLeft,p=r.offsetTop)}return{width:i,height:a,x:s+D(e),y:p}}(e,o)):y(t)?function(e,t){var o=E(e,!1,"fixed"===t);return o.top=o.top+e.clientTop,o.left=o.left+e.clientLeft,o.bottom=o.top+e.clientHeight,o.right=o.left+e.clientWidth,o.width=e.clientWidth,o.height=e.clientHeight,o.x=o.left,o.y=o.top,o}(t,o):xe(function(e){var t,o=k(e),n=M(e),r=null==(t=e.ownerDocument)?void 0:t.body,i=O(o.scrollWidth,o.clientWidth,r?r.scrollWidth:0,r?r.clientWidth:0),a=O(o.scrollHeight,o.clientHeight,r?r.scrollHeight:0,r?r.clientHeight:0),s=-n.scrollLeft+D(e),p=-n.scrollTop;return"rtl"===L(r||o).direction&&(s+=O(o.clientWidth,r?r.clientWidth:0)-i),{width:i,height:a,x:s,y:p}}(k(e)))}function Te(e,t,o,n){var r="clippingParents"===t?function(e){var t=H(W(e)),o=["absolute","fixed"].indexOf(L(e).position)>=0&&w(e)?I(e):e;return y(o)?t.filter((function(e){return y(e)&&we(e,o)&&"body"!==j(e)})):[]}(e):[].concat(t),i=[].concat(r,[o]),a=i[0],s=i.reduce((function(t,o){var r=Oe(e,o,n);return t.top=O(r.top,t.top),t.right=T(r.right,t.right),t.bottom=T(r.bottom,t.bottom),t.left=O(r.left,t.left),t}),Oe(e,a,n));return s.width=s.right-s.left,s.height=s.bottom-s.top,s.x=s.left,s.y=s.top,s}function Pe(e){return Object.assign({},{top:0,right:0,bottom:0,left:0},e)}function Ze(e,t){return t.reduce((function(t,o){return t[o]=e,t}),{})}function Re(e,t){void 0===t&&(t={});var o=t,n=o.placement,r=void 0===n?e.placement:n,i=o.strategy,a=void 0===i?e.strategy:i,s=o.boundary,p=void 0===s?G:s,l=o.rootBoundary,c=void 0===l?J:l,u=o.elementContext,f=void 0===u?K:u,d=o.altBoundary,m=void 0!==d&&d,h=o.padding,v=void 0===h?0:h,g=Pe("number"!==typeof v?v:Ze(v,X)),b=f===K?Q:K,w=e.rects.popper,x=e.elements[m?b:f],O=Te(y(x)?x:x.contextElement||k(e.elements.popper),p,c,a),T=E(e.elements.reference),P=fe({reference:T,element:w,strategy:"absolute",placement:r}),Z=xe(Object.assign({},w,P)),R=f===K?Z:T,M={top:O.top-R.top+g.top,bottom:R.bottom-O.bottom+g.bottom,left:O.left-R.left+g.left,right:R.right-O.right+g.right},j=e.modifiersData.offset;if(f===K&&j){var D=j[r];Object.keys(M).forEach((function(e){var t=[q,V].indexOf(e)>=0?1:-1,o=[$,V].indexOf(e)>=0?"y":"x";M[e]+=D[o]*t}))}return M}function Ee(e,t,o){return O(e,T(t,o))}const Me={name:"preventOverflow",enabled:!0,phase:"main",fn:function(e){var t=e.state,o=e.options,n=e.name,r=o.mainAxis,i=void 0===r||r,a=o.altAxis,s=void 0!==a&&a,p=o.boundary,l=o.rootBoundary,c=o.altBoundary,u=o.padding,f=o.tether,d=void 0===f||f,m=o.tetherOffset,h=void 0===m?0:m,v=Re(t,{boundary:p,rootBoundary:l,padding:u,altBoundary:c}),g=le(t.placement),b=ce(t.placement),y=!b,w=ue(g),x="x"===w?"y":"x",P=t.modifiersData.popperOffsets,Z=t.rects.reference,R=t.rects.popper,E="function"===typeof h?h(Object.assign({},t.rects,{placement:t.placement})):h,M="number"===typeof E?{mainAxis:E,altAxis:E}:Object.assign({mainAxis:0,altAxis:0},E),j=t.modifiersData.offset?t.modifiersData.offset[t.placement]:null,k={x:0,y:0};if(P){if(i){var D,L="y"===w?$:U,A="y"===w?V:q,S="y"===w?"height":"width",W=P[w],B=W+v[L],H=W-v[A],N=d?-R[S]/2:0,F=b===Y?Z[S]:R[S],z=b===Y?-R[S]:-Z[S],X=t.elements.arrow,_=d&&X?C(X):{width:0,height:0},G=t.modifiersData["arrow#persistent"]?t.modifiersData["arrow#persistent"].padding:{top:0,right:0,bottom:0,left:0},J=G[L],K=G[A],Q=Ee(0,Z[S],_[S]),ee=y?Z[S]/2-N-Q-J-M.mainAxis:F-Q-J-M.mainAxis,te=y?-Z[S]/2+N+Q+K+M.mainAxis:z+Q+K+M.mainAxis,oe=t.elements.arrow&&I(t.elements.arrow),ne=oe?"y"===w?oe.clientTop||0:oe.clientLeft||0:0,re=null!=(D=null==j?void 0:j[w])?D:0,ie=W+te-re,ae=Ee(d?T(B,W+ee-re-ne):B,W,d?O(H,ie):H);P[w]=ae,k[w]=ae-W}if(s){var se,pe="x"===w?$:U,fe="x"===w?V:q,de=P[x],me="y"===x?"height":"width",he=de+v[pe],ve=de-v[fe],ge=-1!==[$,U].indexOf(g),be=null!=(se=null==j?void 0:j[x])?se:0,ye=ge?he:de-Z[me]-R[me]-be+M.altAxis,we=ge?de+Z[me]+R[me]-be-M.altAxis:ve,xe=d&&ge?function(e,t,o){var n=Ee(e,t,o);return n>o?o:n}(ye,de,we):Ee(d?ye:he,de,d?we:ve);P[x]=xe,k[x]=xe-de}t.modifiersData[n]=k}},requiresIfExists:["offset"]};const je={name:"arrow",enabled:!0,phase:"main",fn:function(e){var t,o=e.state,n=e.name,r=e.options,i=o.elements.arrow,a=o.modifiersData.popperOffsets,s=le(o.placement),p=ue(s),l=[U,q].indexOf(s)>=0?"height":"width";if(i&&a){var c=function(e,t){return Pe("number"!==typeof(e="function"===typeof e?e(Object.assign({},t.rects,{placement:t.placement})):e)?e:Ze(e,X))}(r.padding,o),u=C(i),f="y"===p?$:U,d="y"===p?V:q,m=o.rects.reference[l]+o.rects.reference[p]-a[p]-o.rects.popper[l],h=a[p]-o.rects.reference[p],v=I(i),g=v?"y"===p?v.clientHeight||0:v.clientWidth||0:0,b=m/2-h/2,y=c[f],w=g-u[l]-c[d],x=g/2-u[l]/2+b,O=Ee(y,x,w),T=p;o.modifiersData[n]=((t={})[T]=O,t.centerOffset=O-x,t)}},effect:function(e){var t=e.state,o=e.options.element,n=void 0===o?"[data-popper-arrow]":o;null!=n&&("string"!==typeof n||(n=t.elements.popper.querySelector(n)))&&we(t.elements.popper,n)&&(t.elements.arrow=n)},requires:["popperOffsets"],requiresIfExists:["preventOverflow"]};function ke(e,t,o){return void 0===o&&(o={x:0,y:0}),{top:e.top-t.height-o.y,right:e.right-t.width+o.x,bottom:e.bottom-t.height+o.y,left:e.left-t.width-o.x}}function De(e){return[$,q,V,U].some((function(t){return e[t]>=0}))}var Le=se({defaultModifiers:[{name:"eventListeners",enabled:!0,phase:"write",fn:function(){},effect:function(e){var t=e.state,o=e.instance,n=e.options,r=n.scroll,i=void 0===r||r,a=n.resize,s=void 0===a||a,p=b(t.elements.popper),l=[].concat(t.scrollParents.reference,t.scrollParents.popper);return i&&l.forEach((function(e){e.addEventListener("scroll",o.update,pe)})),s&&p.addEventListener("resize",o.update,pe),function(){i&&l.forEach((function(e){e.removeEventListener("scroll",o.update,pe)})),s&&p.removeEventListener("resize",o.update,pe)}},data:{}},{name:"popperOffsets",enabled:!0,phase:"read",fn:function(e){var t=e.state,o=e.name;t.modifiersData[o]=fe({reference:t.rects.reference,element:t.rects.popper,strategy:"absolute",placement:t.placement})},data:{}},{name:"computeStyles",enabled:!0,phase:"beforeWrite",fn:function(e){var t=e.state,o=e.options,n=o.gpuAcceleration,r=void 0===n||n,i=o.adaptive,a=void 0===i||i,s=o.roundOffsets,p=void 0===s||s,l={placement:le(t.placement),variation:ce(t.placement),popper:t.elements.popper,popperRect:t.rects.popper,gpuAcceleration:r,isFixed:"fixed"===t.options.strategy};null!=t.modifiersData.popperOffsets&&(t.styles.popper=Object.assign({},t.styles.popper,me(Object.assign({},l,{offsets:t.modifiersData.popperOffsets,position:t.options.strategy,adaptive:a,roundOffsets:p})))),null!=t.modifiersData.arrow&&(t.styles.arrow=Object.assign({},t.styles.arrow,me(Object.assign({},l,{offsets:t.modifiersData.arrow,position:"absolute",adaptive:!1,roundOffsets:p})))),t.attributes.popper=Object.assign({},t.attributes.popper,{"data-popper-placement":t.placement})},data:{}},{name:"applyStyles",enabled:!0,phase:"write",fn:function(e){var t=e.state;Object.keys(t.elements).forEach((function(e){var o=t.styles[e]||{},n=t.attributes[e]||{},r=t.elements[e];w(r)&&j(r)&&(Object.assign(r.style,o),Object.keys(n).forEach((function(e){var t=n[e];!1===t?r.removeAttribute(e):r.setAttribute(e,!0===t?"":t)})))}))},effect:function(e){var t=e.state,o={popper:{position:t.options.strategy,left:"0",top:"0",margin:"0"},arrow:{position:"absolute"},reference:{}};return Object.assign(t.elements.popper.style,o.popper),t.styles=o,t.elements.arrow&&Object.assign(t.elements.arrow.style,o.arrow),function(){Object.keys(t.elements).forEach((function(e){var n=t.elements[e],r=t.attributes[e]||{},i=Object.keys(t.styles.hasOwnProperty(e)?t.styles[e]:o[e]).reduce((function(e,t){return e[t]="",e}),{});w(n)&&j(n)&&(Object.assign(n.style,i),Object.keys(r).forEach((function(e){n.removeAttribute(e)})))}))}},requires:["computeStyles"]},he,{name:"flip",enabled:!0,phase:"main",fn:function(e){var t=e.state,o=e.options,n=e.name;if(!t.modifiersData[n]._skip){for(var r=o.mainAxis,i=void 0===r||r,a=o.altAxis,s=void 0===a||a,p=o.fallbackPlacements,l=o.padding,c=o.boundary,u=o.rootBoundary,f=o.altBoundary,d=o.flipVariations,m=void 0===d||d,h=o.allowedAutoPlacements,v=t.options.placement,g=le(v),b=p||(g===v||!m?[ge(v)]:function(e){if(le(e)===z)return[];var t=ge(e);return[ye(e),t,ye(t)]}(v)),y=[v].concat(b).reduce((function(e,o){return e.concat(le(o)===z?function(e,t){void 0===t&&(t={});var o=t,n=o.placement,r=o.boundary,i=o.rootBoundary,a=o.padding,s=o.flipVariations,p=o.allowedAutoPlacements,l=void 0===p?te:p,c=ce(n),u=c?s?ee:ee.filter((function(e){return ce(e)===c})):X,f=u.filter((function(e){return l.indexOf(e)>=0}));0===f.length&&(f=u);var d=f.reduce((function(t,o){return t[o]=Re(e,{placement:o,boundary:r,rootBoundary:i,padding:a})[le(o)],t}),{});return Object.keys(d).sort((function(e,t){return d[e]-d[t]}))}(t,{placement:o,boundary:c,rootBoundary:u,padding:l,flipVariations:m,allowedAutoPlacements:h}):o)}),[]),w=t.rects.reference,x=t.rects.popper,O=new Map,T=!0,P=y[0],Z=0;Z<y.length;Z++){var R=y[Z],E=le(R),M=ce(R)===Y,j=[$,V].indexOf(E)>=0,k=j?"width":"height",D=Re(t,{placement:R,boundary:c,rootBoundary:u,altBoundary:f,padding:l}),L=j?M?q:U:M?V:$;w[k]>x[k]&&(L=ge(L));var A=ge(L),S=[];if(i&&S.push(D[E]<=0),s&&S.push(D[L]<=0,D[A]<=0),S.every((function(e){return e}))){P=R,T=!1;break}O.set(R,S)}if(T)for(var C=function(e){var t=y.find((function(t){var o=O.get(t);if(o)return o.slice(0,e).every((function(e){return e}))}));if(t)return P=t,"break"},W=m?3:1;W>0;W--){if("break"===C(W))break}t.placement!==P&&(t.modifiersData[n]._skip=!0,t.placement=P,t.reset=!0)}},requiresIfExists:["offset"],data:{_skip:!1}},Me,je,{name:"hide",enabled:!0,phase:"main",requiresIfExists:["preventOverflow"],fn:function(e){var t=e.state,o=e.name,n=t.rects.reference,r=t.rects.popper,i=t.modifiersData.preventOverflow,a=Re(t,{elementContext:"reference"}),s=Re(t,{altBoundary:!0}),p=ke(a,n),l=ke(s,r,i),c=De(p),u=De(l);t.modifiersData[o]={referenceClippingOffsets:p,popperEscapeOffsets:l,isReferenceHidden:c,hasPopperEscaped:u},t.attributes.popper=Object.assign({},t.attributes.popper,{"data-popper-reference-hidden":c,"data-popper-escaped":u})}}]}),Ae=o(96174),Se=o(21217),Ce=o(75878);function We(e){return(0,Se.Z)("MuiPopper",e)}(0,Ce.Z)("MuiPopper",["root"]);var Be=o(41107),He=o(80184);const Ne={disableDefaultClasses:!1},Fe=i.createContext(Ne);const Ie=["anchorEl","children","direction","disablePortal","modifiers","open","placement","popperOptions","popperRef","slotProps","slots","TransitionProps","ownerState"],$e=["anchorEl","children","container","direction","disablePortal","keepMounted","modifiers","open","placement","popperOptions","popperRef","style","transition","slotProps","slots"];function Ve(e){return"function"===typeof e?e():e}function qe(e){return void 0!==e.nodeType}const Ue=()=>(0,s.Z)({root:["root"]},function(e){const{disableDefaultClasses:t}=i.useContext(Fe);return o=>t?"":e(o)}(We)),ze={},Xe=i.forwardRef((function(e,t){var o;const{anchorEl:a,children:s,direction:p,disablePortal:l,modifiers:c,open:u,placement:f,popperOptions:d,popperRef:m,slotProps:g={},slots:b={},TransitionProps:y}=e,w=(0,n.Z)(e,Ie),x=i.useRef(null),O=(0,h.Z)(x,t),T=i.useRef(null),P=(0,h.Z)(T,m),Z=i.useRef(P);(0,v.Z)((()=>{Z.current=P}),[P]),i.useImperativeHandle(m,(()=>T.current),[]);const R=function(e,t){if("ltr"===t)return e;switch(e){case"bottom-end":return"bottom-start";case"bottom-start":return"bottom-end";case"top-end":return"top-start";case"top-start":return"top-end";default:return e}}(f,p),[E,M]=i.useState(R),[j,k]=i.useState(Ve(a));i.useEffect((()=>{T.current&&T.current.forceUpdate()})),i.useEffect((()=>{a&&k(Ve(a))}),[a]),(0,v.Z)((()=>{if(!j||!u)return;let e=[{name:"preventOverflow",options:{altBoundary:l}},{name:"flip",options:{altBoundary:l}},{name:"onUpdate",enabled:!0,phase:"afterWrite",fn:e=>{let{state:t}=e;M(t.placement)}}];null!=c&&(e=e.concat(c)),d&&null!=d.modifiers&&(e=e.concat(d.modifiers));const t=Le(j,x.current,(0,r.Z)({placement:R},d,{modifiers:e}));return Z.current(t),()=>{t.destroy(),Z.current(null)}}),[j,l,c,u,d,R]);const D={placement:E};null!==y&&(D.TransitionProps=y);const L=Ue(),A=null!=(o=b.root)?o:"div",S=(0,Be.y)({elementType:A,externalSlotProps:g.root,externalForwardedProps:w,additionalProps:{role:"tooltip",ref:O},ownerState:e,className:L.root});return(0,He.jsx)(A,(0,r.Z)({},S,{children:"function"===typeof s?s(D):s}))})),Ye=i.forwardRef((function(e,t){const{anchorEl:o,children:a,container:s,direction:p="ltr",disablePortal:l=!1,keepMounted:c=!1,modifiers:u,open:f,placement:d="bottom",popperOptions:m=ze,popperRef:h,style:v,transition:b=!1,slotProps:y={},slots:w={}}=e,x=(0,n.Z)(e,$e),[O,T]=i.useState(!0);if(!c&&!f&&(!b||O))return null;let P;if(s)P=s;else if(o){const e=Ve(o);P=e&&qe(e)?(0,g.Z)(e).body:(0,g.Z)(null).body}const Z=f||!c||b&&!O?void 0:"none",R=b?{in:f,onEnter:()=>{T(!1)},onExited:()=>{T(!0)}}:void 0;return(0,He.jsx)(Ae.h,{disablePortal:l,container:P,children:(0,He.jsx)(Xe,(0,r.Z)({anchorEl:o,direction:p,disablePortal:l,modifiers:u,ref:t,open:b?!O:f,placement:d,popperOptions:m,popperRef:h,slotProps:y,slots:w},x,{style:(0,r.Z)({position:"fixed",top:0,left:0,display:Z},v),TransitionProps:R,children:a}))})}));var _e=o(69120);const Ge=["anchorEl","component","components","componentsProps","container","disablePortal","keepMounted","modifiers","open","placement","popperOptions","popperRef","transition","slots","slotProps"],Je=(0,c.ZP)(Ye,{name:"MuiPopper",slot:"Root",overridesResolver:(e,t)=>t.root})({}),Ke=i.forwardRef((function(e,t){var o;const i=(0,_e.Z)(),a=(0,f.Z)({props:e,name:"MuiPopper"}),{anchorEl:s,component:p,components:l,componentsProps:c,container:u,disablePortal:d,keepMounted:m,modifiers:h,open:v,placement:g,popperOptions:b,popperRef:y,transition:w,slots:x,slotProps:O}=a,T=(0,n.Z)(a,Ge),P=null!=(o=null==x?void 0:x.root)?o:null==l?void 0:l.Root,Z=(0,r.Z)({anchorEl:s,container:u,disablePortal:d,keepMounted:m,modifiers:h,open:v,placement:g,popperOptions:b,popperRef:y,transition:w},T);return(0,He.jsx)(Je,(0,r.Z)({as:p,direction:null==i?void 0:i.direction,slots:{root:P},slotProps:null!=O?O:c},Z,{ref:t}))}));var Qe=o(89683),et=o(42071),tt=o(67384),ot=o(23031),nt=o(5158);function rt(e){return(0,Se.Z)("MuiTooltip",e)}const it=(0,Ce.Z)("MuiTooltip",["popper","popperInteractive","popperArrow","popperClose","tooltip","tooltipArrow","touch","tooltipPlacementLeft","tooltipPlacementRight","tooltipPlacementTop","tooltipPlacementBottom","arrow"]),at=["arrow","children","classes","components","componentsProps","describeChild","disableFocusListener","disableHoverListener","disableInteractive","disableTouchListener","enterDelay","enterNextDelay","enterTouchDelay","followCursor","id","leaveDelay","leaveTouchDelay","onClose","onOpen","open","placement","PopperComponent","PopperProps","slotProps","slots","title","TransitionComponent","TransitionProps"];const st=(0,c.ZP)(Ke,{name:"MuiTooltip",slot:"Popper",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.popper,!o.disableInteractive&&t.popperInteractive,o.arrow&&t.popperArrow,!o.open&&t.popperClose]}})((e=>{let{theme:t,ownerState:o,open:n}=e;return(0,r.Z)({zIndex:(t.vars||t).zIndex.tooltip,pointerEvents:"none"},!o.disableInteractive&&{pointerEvents:"auto"},!n&&{pointerEvents:"none"},o.arrow&&{[`&[data-popper-placement*="bottom"] .${it.arrow}`]:{top:0,marginTop:"-0.71em","&::before":{transformOrigin:"0 100%"}},[`&[data-popper-placement*="top"] .${it.arrow}`]:{bottom:0,marginBottom:"-0.71em","&::before":{transformOrigin:"100% 0"}},[`&[data-popper-placement*="right"] .${it.arrow}`]:(0,r.Z)({},o.isRtl?{right:0,marginRight:"-0.71em"}:{left:0,marginLeft:"-0.71em"},{height:"1em",width:"0.71em","&::before":{transformOrigin:"100% 100%"}}),[`&[data-popper-placement*="left"] .${it.arrow}`]:(0,r.Z)({},o.isRtl?{left:0,marginLeft:"-0.71em"}:{right:0,marginRight:"-0.71em"},{height:"1em",width:"0.71em","&::before":{transformOrigin:"0 0"}})})})),pt=(0,c.ZP)("div",{name:"MuiTooltip",slot:"Tooltip",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.tooltip,o.touch&&t.touch,o.arrow&&t.tooltipArrow,t[`tooltipPlacement${(0,d.Z)(o.placement.split("-")[0])}`]]}})((e=>{let{theme:t,ownerState:o}=e;return(0,r.Z)({backgroundColor:t.vars?t.vars.palette.Tooltip.bg:(0,l.Fq)(t.palette.grey[700],.92),borderRadius:(t.vars||t).shape.borderRadius,color:(t.vars||t).palette.common.white,fontFamily:t.typography.fontFamily,padding:"4px 8px",fontSize:t.typography.pxToRem(11),maxWidth:300,margin:2,wordWrap:"break-word",fontWeight:t.typography.fontWeightMedium},o.arrow&&{position:"relative",margin:0},o.touch&&{padding:"8px 16px",fontSize:t.typography.pxToRem(14),lineHeight:(n=16/14,Math.round(1e5*n)/1e5)+"em",fontWeight:t.typography.fontWeightRegular},{[`.${it.popper}[data-popper-placement*="left"] &`]:(0,r.Z)({transformOrigin:"right center"},o.isRtl?(0,r.Z)({marginLeft:"14px"},o.touch&&{marginLeft:"24px"}):(0,r.Z)({marginRight:"14px"},o.touch&&{marginRight:"24px"})),[`.${it.popper}[data-popper-placement*="right"] &`]:(0,r.Z)({transformOrigin:"left center"},o.isRtl?(0,r.Z)({marginRight:"14px"},o.touch&&{marginRight:"24px"}):(0,r.Z)({marginLeft:"14px"},o.touch&&{marginLeft:"24px"})),[`.${it.popper}[data-popper-placement*="top"] &`]:(0,r.Z)({transformOrigin:"center bottom",marginBottom:"14px"},o.touch&&{marginBottom:"24px"}),[`.${it.popper}[data-popper-placement*="bottom"] &`]:(0,r.Z)({transformOrigin:"center top",marginTop:"14px"},o.touch&&{marginTop:"24px"})});var n})),lt=(0,c.ZP)("span",{name:"MuiTooltip",slot:"Arrow",overridesResolver:(e,t)=>t.arrow})((e=>{let{theme:t}=e;return{overflow:"hidden",position:"absolute",width:"1em",height:"0.71em",boxSizing:"border-box",color:t.vars?t.vars.palette.Tooltip.bg:(0,l.Fq)(t.palette.grey[700],.9),"&::before":{content:'""',margin:"auto",display:"block",width:"100%",height:"100%",backgroundColor:"currentColor",transform:"rotate(45deg)"}}}));let ct=!1,ut=null,ft={x:0,y:0};function dt(e,t){return o=>{t&&t(o),e(o)}}const mt=i.forwardRef((function(e,t){var o,l,c,h,v,g,b,y,w,x,O,T,P,Z,R,E,M,j,k;const D=(0,f.Z)({props:e,name:"MuiTooltip"}),{arrow:L=!1,children:A,components:S={},componentsProps:C={},describeChild:W=!1,disableFocusListener:B=!1,disableHoverListener:H=!1,disableInteractive:N=!1,disableTouchListener:F=!1,enterDelay:I=100,enterNextDelay:$=0,enterTouchDelay:V=700,followCursor:q=!1,id:U,leaveDelay:z=0,leaveTouchDelay:X=1500,onClose:Y,onOpen:_,open:G,placement:J="bottom",PopperComponent:K,PopperProps:Q={},slotProps:ee={},slots:te={},title:oe,TransitionComponent:ne=m.Z,TransitionProps:re}=D,ie=(0,n.Z)(D,at),ae=i.isValidElement(A)?A:(0,He.jsx)("span",{children:A}),se=(0,u.Z)(),pe="rtl"===se.direction,[le,ce]=i.useState(),[ue,fe]=i.useState(null),de=i.useRef(!1),me=N||q,he=i.useRef(),ve=i.useRef(),ge=i.useRef(),be=i.useRef(),[ye,we]=(0,nt.Z)({controlled:G,default:!1,name:"Tooltip",state:"open"});let xe=ye;const Oe=(0,tt.Z)(U),Te=i.useRef(),Pe=i.useCallback((()=>{void 0!==Te.current&&(document.body.style.WebkitUserSelect=Te.current,Te.current=void 0),clearTimeout(be.current)}),[]);i.useEffect((()=>()=>{clearTimeout(he.current),clearTimeout(ve.current),clearTimeout(ge.current),Pe()}),[Pe]);const Ze=e=>{clearTimeout(ut),ct=!0,we(!0),_&&!xe&&_(e)},Re=(0,Qe.Z)((e=>{clearTimeout(ut),ut=setTimeout((()=>{ct=!1}),800+z),we(!1),Y&&xe&&Y(e),clearTimeout(he.current),he.current=setTimeout((()=>{de.current=!1}),se.transitions.duration.shortest)})),Ee=e=>{de.current&&"touchstart"!==e.type||(le&&le.removeAttribute("title"),clearTimeout(ve.current),clearTimeout(ge.current),I||ct&&$?ve.current=setTimeout((()=>{Ze(e)}),ct?$:I):Ze(e))},Me=e=>{clearTimeout(ve.current),clearTimeout(ge.current),ge.current=setTimeout((()=>{Re(e)}),z)},{isFocusVisibleRef:je,onBlur:ke,onFocus:De,ref:Le}=(0,ot.Z)(),[,Ae]=i.useState(!1),Se=e=>{ke(e),!1===je.current&&(Ae(!1),Me(e))},Ce=e=>{le||ce(e.currentTarget),De(e),!0===je.current&&(Ae(!0),Ee(e))},We=e=>{de.current=!0;const t=ae.props;t.onTouchStart&&t.onTouchStart(e)},Be=Ee,Ne=Me,Fe=e=>{We(e),clearTimeout(ge.current),clearTimeout(he.current),Pe(),Te.current=document.body.style.WebkitUserSelect,document.body.style.WebkitUserSelect="none",be.current=setTimeout((()=>{document.body.style.WebkitUserSelect=Te.current,Ee(e)}),V)},Ie=e=>{ae.props.onTouchEnd&&ae.props.onTouchEnd(e),Pe(),clearTimeout(ge.current),ge.current=setTimeout((()=>{Re(e)}),X)};i.useEffect((()=>{if(xe)return document.addEventListener("keydown",e),()=>{document.removeEventListener("keydown",e)};function e(e){"Escape"!==e.key&&"Esc"!==e.key||Re(e)}}),[Re,xe]);const $e=(0,et.Z)(ae.ref,Le,ce,t);oe||0===oe||(xe=!1);const Ve=i.useRef(),qe={},Ue="string"===typeof oe;W?(qe.title=xe||!Ue||H?null:oe,qe["aria-describedby"]=xe?Oe:null):(qe["aria-label"]=Ue?oe:null,qe["aria-labelledby"]=xe&&!Ue?Oe:null);const ze=(0,r.Z)({},qe,ie,ae.props,{className:(0,a.Z)(ie.className,ae.props.className),onTouchStart:We,ref:$e},q?{onMouseMove:e=>{const t=ae.props;t.onMouseMove&&t.onMouseMove(e),ft={x:e.clientX,y:e.clientY},Ve.current&&Ve.current.update()}}:{});const Xe={};F||(ze.onTouchStart=Fe,ze.onTouchEnd=Ie),H||(ze.onMouseOver=dt(Be,ze.onMouseOver),ze.onMouseLeave=dt(Ne,ze.onMouseLeave),me||(Xe.onMouseOver=Be,Xe.onMouseLeave=Ne)),B||(ze.onFocus=dt(Ce,ze.onFocus),ze.onBlur=dt(Se,ze.onBlur),me||(Xe.onFocus=Ce,Xe.onBlur=Se));const Ye=i.useMemo((()=>{var e;let t=[{name:"arrow",enabled:Boolean(ue),options:{element:ue,padding:4}}];return null!=(e=Q.popperOptions)&&e.modifiers&&(t=t.concat(Q.popperOptions.modifiers)),(0,r.Z)({},Q.popperOptions,{modifiers:t})}),[ue,Q]),_e=(0,r.Z)({},D,{isRtl:pe,arrow:L,disableInteractive:me,placement:J,PopperComponentProp:K,touch:de.current}),Ge=(e=>{const{classes:t,disableInteractive:o,arrow:n,touch:r,placement:i}=e,a={popper:["popper",!o&&"popperInteractive",n&&"popperArrow"],tooltip:["tooltip",n&&"tooltipArrow",r&&"touch",`tooltipPlacement${(0,d.Z)(i.split("-")[0])}`],arrow:["arrow"]};return(0,s.Z)(a,rt,t)})(_e),Je=null!=(o=null!=(l=te.popper)?l:S.Popper)?o:st,it=null!=(c=null!=(h=null!=(v=te.transition)?v:S.Transition)?h:ne)?c:m.Z,mt=null!=(g=null!=(b=te.tooltip)?b:S.Tooltip)?g:pt,ht=null!=(y=null!=(w=te.arrow)?w:S.Arrow)?y:lt,vt=(0,p.$)(Je,(0,r.Z)({},Q,null!=(x=ee.popper)?x:C.popper,{className:(0,a.Z)(Ge.popper,null==Q?void 0:Q.className,null==(O=null!=(T=ee.popper)?T:C.popper)?void 0:O.className)}),_e),gt=(0,p.$)(it,(0,r.Z)({},re,null!=(P=ee.transition)?P:C.transition),_e),bt=(0,p.$)(mt,(0,r.Z)({},null!=(Z=ee.tooltip)?Z:C.tooltip,{className:(0,a.Z)(Ge.tooltip,null==(R=null!=(E=ee.tooltip)?E:C.tooltip)?void 0:R.className)}),_e),yt=(0,p.$)(ht,(0,r.Z)({},null!=(M=ee.arrow)?M:C.arrow,{className:(0,a.Z)(Ge.arrow,null==(j=null!=(k=ee.arrow)?k:C.arrow)?void 0:j.className)}),_e);return(0,He.jsxs)(i.Fragment,{children:[i.cloneElement(ae,ze),(0,He.jsx)(Je,(0,r.Z)({as:null!=K?K:Ke,placement:J,anchorEl:q?{getBoundingClientRect:()=>({top:ft.y,left:ft.x,right:ft.x,bottom:ft.y,width:0,height:0})}:le,popperRef:Ve,open:!!le&&xe,id:Oe,transition:!0},Xe,vt,{popperOptions:Ye,children:e=>{let{TransitionProps:t}=e;return(0,He.jsx)(it,(0,r.Z)({timeout:se.transitions.duration.shorter},t,gt,{children:(0,He.jsxs)(mt,(0,r.Z)({},bt,{children:[oe,L?(0,He.jsx)(ht,(0,r.Z)({},yt,{ref:fe})):null]}))}))}}))]})})),ht=mt}}]);