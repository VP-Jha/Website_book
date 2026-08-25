const root=document.documentElement;
const header=document.querySelector('[data-header]');
const menuButton=document.querySelector('.menu-button');
const navigation=document.querySelector('.site-nav');
const themeButton=document.querySelector('[data-theme-toggle]');

document.body.classList.toggle('home',location.pathname.endsWith('/')||location.pathname.endsWith('index.html'));
const savedTheme=localStorage.getItem('vpj-theme');
if(savedTheme==='dark'||savedTheme==='light')root.dataset.theme=savedTheme;
const setThemeLabel=()=>{if(themeButton)themeButton.setAttribute('aria-label',root.dataset.theme==='dark'?'Switch to light theme':'Switch to dark theme')};
setThemeLabel();
themeButton?.addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem('vpj-theme',root.dataset.theme);setThemeLabel()});

const setHeaderState=()=>header?.classList.toggle('is-scrolled',window.scrollY>18);
setHeaderState();window.addEventListener('scroll',setHeaderState,{passive:true});
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')==='true';menuButton.setAttribute('aria-expanded',String(!open));navigation?.classList.toggle('is-open',!open)});
navigation?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{menuButton?.setAttribute('aria-expanded','false');navigation.classList.remove('is-open')}));

const caption=document.querySelector('[data-concept-caption]');
document.querySelectorAll('[data-concept]').forEach(concept=>{const activate=()=>{document.querySelectorAll('[data-concept]').forEach(item=>item.classList.remove('is-active'));concept.classList.add('is-active');if(caption)caption.textContent=concept.dataset.concept};concept.addEventListener('mouseenter',activate);concept.addEventListener('focus',activate)});

const searchInput=document.querySelector('[data-blog-search]');
const filterButtons=[...document.querySelectorAll('[data-filter]')];
const blogItems=[...document.querySelectorAll('[data-blog-item]')];
const noResults=document.querySelector('[data-no-results]');
let activeTopic='all';
const filterBlog=()=>{const query=(searchInput?.value||'').trim().toLowerCase();let visible=0;blogItems.forEach(item=>{const show=(activeTopic==='all'||item.dataset.topic===activeTopic)&&(!query||item.dataset.search.toLowerCase().includes(query));item.classList.toggle('is-hidden',!show);if(show)visible++});noResults?.classList.toggle('is-visible',visible===0)};
filterButtons.forEach(button=>button.addEventListener('click',()=>{activeTopic=button.dataset.filter;filterButtons.forEach(item=>{const active=item===button;item.classList.toggle('is-active',active);item.setAttribute('aria-pressed',String(active))});filterBlog()}));
searchInput?.addEventListener('input',filterBlog);
if(filterButtons.length){const topic=new URLSearchParams(location.search).get('topic');filterButtons.find(button=>button.dataset.filter===topic)?.click()}
document.addEventListener('keydown',event=>{if(event.key==='/'&&searchInput&&document.activeElement!==searchInput){event.preventDefault();searchInput.focus()}});

const progress=document.querySelector('[data-reading-progress]');
if(progress){const update=()=>{const max=document.documentElement.scrollHeight-innerHeight;progress.style.width=`${max>0?Math.min(100,scrollY/max*100):0}%`};update();addEventListener('scroll',update,{passive:true})}
document.querySelectorAll('[data-share]').forEach(button=>button.addEventListener('click',async()=>{const action=button.dataset.share,url=location.href,title=document.title;if(action==='native'&&navigator.share){await navigator.share({title,url})}else if(action==='copy'){await navigator.clipboard.writeText(url);const original=button.textContent;button.textContent='✓';setTimeout(()=>{button.textContent=original},1600)}else if(action==='x'){window.open(`https://x.com/intent/post?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`,'_blank','noopener')}}));

if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target)}}),{threshold:.1});document.querySelectorAll('.reveal').forEach(element=>observer.observe(element))}else{document.querySelectorAll('.reveal').forEach(element=>element.classList.add('is-visible'))}
document.querySelectorAll('[data-year]').forEach(element=>{element.textContent=new Date().getFullYear()});
