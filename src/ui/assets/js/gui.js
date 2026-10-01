
        function switchPage(pageId, el) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            const navBtn = el || document.querySelector(`.nav-btn[data-page="${pageId}"]`);
            if (navBtn) navBtn.classList.add('active');

            const pageTitles = { account: 'Overview', console: 'Console', rpc: 'Rich Presence', commands: 'Commands', info: 'About', config: 'Settings' };
            const header = document.getElementById('page-header');
            const headerTitle = document.getElementById('page-header-title');
            if (header) header.hidden = pageId === 'account';
            if (headerTitle && pageTitles[pageId]) headerTitle.innerText = pageTitles[pageId];

            if (pageId === 'account') setTimeout(resizeBadgeBox, 50);
            if (pageId === 'rpc') {
                loadRpcConfig();
                loadDiscordProfile();
            }
            if (pageId === 'commands') loadCommands();
        }
        function goPage(pageId) { switchPage(pageId, null); }
        function switchConfig(sectionId, el) {
            document.querySelectorAll('.cfg-section').forEach(s => s.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');
            document.querySelectorAll('.cfg-tab').forEach(t => t.classList.remove('active'));
            if (el) el.classList.add('active');
        }

        let currentRpcType = 'rpc';
        let rpcData = {};
        function switchRpcTab(type, el) {
            currentRpcType = type;
            document.querySelectorAll('.rpc-tab').forEach(t => t.classList.remove('active'));
            el.classList.add('active');

            const descEl = document.getElementById('rpc-tab-description');
            if (descEl) {
                switch (type) {
                    case 'rpc':
                        descEl.innerText = 'Custom Discord Rich Presence activity';
                        break;
                    case 'console':
                        descEl.innerText = 'Gaming console presence (PlayStation, Xbox, Switch)';
                        break;
                    case 'spotify':
                        descEl.innerText = 'Fake Spotify listening activity';
                        break;
                }
            }

            loadRpcConfig();
        }
        async function loadRpcConfig() {
            if (typeof window.pywebview === 'undefined' || !window.pywebview.api) return;
            const currentRpc = await config_get('rpc');
            const statusDot = document.getElementById('rpc-status-dot');
            const statusText = document.getElementById('rpc-status-text');
            const enableToggle = document.getElementById('rpc-enable-toggle');
            if (currentRpc) {
                statusText.innerText = 'Active: ' + currentRpc;
                if (statusDot) statusDot.style.color = 'var(--accent)';
                if (enableToggle) enableToggle.checked = true;
            } else {
                statusText.innerText = 'Disabled';
                if (statusDot) statusDot.style.color = 'var(--text-2)';
                if (enableToggle) enableToggle.checked = false;
            }
            setQuickToggle('rpc', !!currentRpc);
            window.pywebview.api.get_rpc_config(currentRpcType).then(data => {
                rpcData = data || {};
                renderRpcFields(currentRpcType, data);
                updateRpcPreview(data, currentRpcType);
            }).catch(e => console.error(e));
        }
        async function applyRpc() {
            try {
                await pywebview.api.apply_rpc();
                return true;
            } catch (e) {
                showNotification('Rich Presence not applied', escapeHtml(String(e.message || e)), 'error');
                return false;
            }
        }
        async function toggleRpcEnabled(enabled) {
            const statusDot = document.getElementById('rpc-status-dot');
            const statusText = document.getElementById('rpc-status-text');
            const enableToggle = document.getElementById('rpc-enable-toggle');
            if (enableToggle) enableToggle.checked = enabled;
            setQuickToggle('rpc', enabled);
            statusText.innerText = enabled ? 'Active: ' + currentRpcType : 'Disabled';
            if (statusDot) statusDot.style.color = enabled ? 'var(--accent)' : 'var(--text-2)';
            await config_edit('rpc', enabled ? currentRpcType : '');
            if (await applyRpc()) {
                pywebview.api.sendnotif(enabled ? 'Rich Presence enabled: ' + currentRpcType : 'Rich Presence disabled');
            }
        }
        function renderRpcFields(type, data) {
            const container = document.getElementById('rpc-fields');
            container.innerHTML = '';
            const statusOpts = ['online','idle','dnd','invisible'];
            if (type === 'rpc') {
                const stateOpts = ['Playing','Streaming','Watching','Competing'];
                const fields = [
                    {key:'Title',label:'Title',type:'input'},
                    {key:'Description',label:'Description',type:'input'},
                    {key:'Large_Image',label:'Large Image',type:'input'},
                    {key:'Small_Image',label:'Small Image',type:'input'},
                    {key:'Large_Image_Text',label:'Large Image Text',type:'input'},
                    {key:'Small_Image_Text',label:'Small Image Text',type:'input'},
                    {key:'State',label:'State',type:'select',opts:stateOpts},
                    {key:'SubText',label:'Sub Text',type:'input'},
                    {key:'Status',label:'Status',type:'select',opts:statusOpts},
                    {key:'Timer',label:'Timer',type:'toggle'},
                    {key:'Watch_Url',label:'Watch URL',type:'input'},
                ];
                fields.forEach(f => container.appendChild(makeRpcField(f, data[f.key])));

                const btnSection = document.createElement('div');
                btnSection.style.cssText = 'margin-top:8px;padding-top:12px;border-top:1px solid var(--border);';
                const btnTitle = document.createElement('div');
                btnTitle.style.cssText = 'font-size:13px;font-weight:600;color:var(--text-1);margin-bottom:8px;';
                btnTitle.innerText = 'Buttons (max 2)';
                btnSection.appendChild(btnTitle);
                const buttons = data && data.Buttons ? data.Buttons : [{label:'',url:''},{label:'',url:''}];
                for (let i = 0; i < 2; i++) {
                    const btn = buttons[i] || {label:'',url:''};
                    const row = document.createElement('div');
                    row.style.cssText = 'display:flex;gap:6px;margin-bottom:6px;align-items:center;';
                    const num = document.createElement('span');
                    num.style.cssText = 'font-size:11px;color:var(--text-2);min-width:18px;';
                    num.innerText = (i+1) + '.';
                    row.appendChild(num);
                    const labelInput = document.createElement('input');
                    labelInput.type = 'text'; labelInput.id = 'rpc-btn-label-' + i;
                    labelInput.value = btn.label || '';
                    labelInput.placeholder = 'Button Label';
                    labelInput.style.cssText = 'flex:1;padding:6px 10px;background:var(--bg-3);border:1px solid var(--border);border-radius:6px;color:var(--text-0);font-size:12px;outline:none;';
                    labelInput.addEventListener('input', () => {
                        updateRpcPreview(getCurrentRpcData(), currentRpcType);
                    });
                    row.appendChild(labelInput);
                    const urlInput = document.createElement('input');
                    urlInput.type = 'text'; urlInput.id = 'rpc-btn-url-' + i;
                    urlInput.value = btn.url || '';
                    urlInput.placeholder = 'Button URL';
                    urlInput.style.cssText = 'flex:1.5;padding:6px 10px;background:var(--bg-3);border:1px solid var(--border);border-radius:6px;color:var(--text-0);font-size:12px;outline:none;';
                    urlInput.addEventListener('input', () => {
                        updateRpcPreview(getCurrentRpcData(), currentRpcType);
                    });
                    row.appendChild(urlInput);
                    btnSection.appendChild(row);
                }
                container.appendChild(btnSection);
            } else if (type === 'console') {
                const fields = [
                    {key:'Title',label:'Title',type:'input'},
                    {key:'Description',label:'Description',type:'input'},
                    {key:'SubText',label:'Sub Text',type:'input'},
                    {key:'Large_Image',label:'Large Image',type:'input'},
                    {key:'Small_Image',label:'Small Image',type:'input'},
                    {key:'Large_Image_Text',label:'Large Image Text',type:'input'},
                    {key:'Small_Image_Text',label:'Small Image Text',type:'input'},
                    {key:'Status',label:'Status',type:'select',opts:statusOpts},
                    {key:'Timer',label:'Timer',type:'toggle'},
                    {key:'Platform',label:'Platform',type:'select',opts:['playstation','xbox','switch']},
                ];
                fields.forEach(f => container.appendChild(makeRpcField(f, data[f.key])));
            } else if (type === 'spotify') {
                const fields = [
                    {key:'SongTitle',label:'Song Title',type:'input'},
                    {key:'ArtistName',label:'Artist',type:'input'},
                    {key:'AlbumName',label:'Album',type:'input'},
                    {key:'Image',label:'Image',type:'input'},
                    {key:'SongLength',label:'Length (sec)',type:'input'},
                    {key:'Status',label:'Status',type:'select',opts:statusOpts},
                    {key:'Buttons',label:'Buttons',type:'toggle'},
                    {key:'albumid',label:'Album ID',type:'input'},
                ];
                fields.forEach(f => container.appendChild(makeRpcField(f, data[f.key])));
            }
        }

        function getCurrentRpcData() {
            const data = {};
            document.querySelectorAll('#rpc-fields input[type="text"]').forEach(i => {
                data[i.id.replace('rpc-input-','')] = i.value;
            });
            document.querySelectorAll('#rpc-fields select').forEach(s => {
                data[s.id.replace('rpc-input-','')] = s.value;
            });
            document.querySelectorAll('#rpc-fields input[type="checkbox"]').forEach(c => {
                data[c.id.replace('rpc-input-','')] = c.checked;
            });

            const buttons = [];
            for (let i = 0; i < 2; i++) {
                const labelInput = document.getElementById('rpc-btn-label-' + i);
                const urlInput = document.getElementById('rpc-btn-url-' + i);
                if (labelInput || urlInput) {
                    buttons.push({
                        label: labelInput ? labelInput.value : '',
                        url: urlInput ? urlInput.value : ''
                    });
                }
            }
            data.Buttons = buttons;
            return data;
        }

        function makeRpcField(f, value) {
            const div = document.createElement('div');
            div.className = 'rpc-field';
            const label = document.createElement('label');
            label.innerText = f.label;
            div.appendChild(label);
            if (f.type === 'input') {
                const input = document.createElement('input');
                input.type = 'text';
                input.id = 'rpc-input-' + f.key;
                input.value = value || '';
                input.placeholder = f.label;
                input.addEventListener('input', () => {
                    updateRpcPreview(getCurrentRpcData(), currentRpcType);
                });
                div.appendChild(input);
            } else if (f.type === 'select') {
                const sel = document.createElement('select');
                sel.id = 'rpc-input-' + f.key;
                f.opts.forEach(o => {
                    const opt = document.createElement('option');
                    opt.value = o;
                    opt.textContent = o;
                    if(o === value) opt.selected = true;
                    sel.appendChild(opt);
                });
                sel.addEventListener('change', () => {
                    updateRpcPreview(getCurrentRpcData(), currentRpcType);
                });
                div.appendChild(sel);
            } else if (f.type === 'toggle') {
                const toggleLabel = document.createElement('label');
                toggleLabel.className = 'toggle-switch';
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.id = 'rpc-input-' + f.key;
                input.checked = Boolean(value);
                input.addEventListener('change', () => {
                    updateRpcPreview(getCurrentRpcData(), currentRpcType);
                });
                const slider = document.createElement('span');
                slider.className = 'slider round';
                toggleLabel.appendChild(input);
                toggleLabel.appendChild(slider);
                div.appendChild(toggleLabel);
            }
            return div;
        }
        function updateRpcPreview(data, type) {
            const title = data.Title || data.SongTitle || '';
            const desc = data.Description || data.ArtistName || '';
            const state = data.SubText || data.AlbumName || '';
            const img = data.Large_Image || data.Image || '';
            const smallImg = data.Small_Image || '';

            const activityCard = document.getElementById('rpc-activity-card');

            const statusDotEl = document.getElementById('rpc-status-indicator-dot');
            if (statusDotEl) {
                statusDotEl.className = 'profile-status-dot status-' + (data.Status || 'online');
            }

            const verbEl = document.getElementById('rpc-activity-verb');
            const iconEl = document.getElementById('rpc-activity-icon');
            if (verbEl && iconEl) {
                if (type === 'spotify') {
                    iconEl.className = 'fa-brands fa-spotify';
                    verbEl.textContent = 'Listening to Spotify';
                } else if (type === 'console') {
                    iconEl.className = 'fa-solid fa-gamepad';
                    verbEl.textContent = 'Playing a Game';
                } else {
                    iconEl.className = 'fa-solid fa-gamepad';
                    verbEl.textContent = (data.State || 'Playing') + (title ? ' ' + title : ' a Game');
                }
            }

            if (type === 'spotify') {

                activityCard.className = 'activity-card spotify-activity-card';
                activityCard.innerHTML = `
                    <div class="spotify-album-art-container">
                        <img class="spotify-album-art" id="rpc-spotify-album" src="${img || ''}" alt="Album Art" />
                    </div>
                    <div class="spotify-info">
                        <div class="spotify-logo"><i class="fa-brands fa-spotify" style="color: #1db954; font-size: 18px;"></i></div>
                        <h4 class="spotify-song-title" id="rpc-activity-name">${title || 'Song Title'}</h4>
                        <p class="spotify-artist" id="rpc-activity-details-text">${desc || 'Artist'}</p>
                        <p class="spotify-album" id="rpc-activity-state">${state || 'Album'}</p>
                        <div class="spotify-scrubber">
                            <div class="spotify-scrubber-progress"></div>
                        </div>
                    </div>
                `;
            } else {
                const platforms = {
                    playstation: { icon: 'fa-brands fa-playstation', bg: '#00439c' },
                    xbox: { icon: 'fa-brands fa-xbox', bg: '#107c10' },
                    switch: { icon: 'fa-solid fa-gamepad', bg: '#e60012' },
                };
                activityCard.className = type === 'console' ? 'activity-card console-activity-card' : 'activity-card';
                buildActivityCard(activityCard, {
                    title, details: desc, state, img, smallImg,
                    timer: Boolean(data.Timer),
                    platform: type === 'console' ? platforms[data.Platform] : null,
                    buttons: type === 'rpc' ? (data.Buttons || []).filter(b => b && b.label) : [],
                });
            }

            const spotifyAlbum = document.getElementById('rpc-spotify-album');
            if (spotifyAlbum) {
                if (img) {
                    spotifyAlbum.src = img;
                    spotifyAlbum.style.display = 'block';
                } else {
                    spotifyAlbum.style.display = 'none';
                }
            }
        }

        function buildActivityCard(card, { title, details, state, img, smallImg, timer, platform, buttons }) {
            const el = (tag, cls, text) => {
                const n = document.createElement(tag);
                if (cls) n.className = cls;
                if (text !== undefined) n.textContent = text;
                return n;
            };
            card.innerHTML = '';

            const images = el('div', 'activity-images');
            const large = el('div', 'large-image-container');
            const largeImg = el('img', 'large-image');
            largeImg.id = 'rpc-large-img';
            largeImg.alt = '';
            const markEmpty = () => { large.classList.add('empty'); large.title = 'No large image: Discord shows a blank square here'; };
            largeImg.onerror = markEmpty;
            if (img) largeImg.src = img; else markEmpty();
            large.onclick = () => editRpcElement('largeImage');
            large.appendChild(largeImg);
            if (platform) {
                const badge = el('div', 'console-platform-badge');
                badge.id = 'rpc-console-platform';
                badge.style.backgroundColor = platform.bg;
                const icon = el('i', platform.icon);
                icon.style.cssText = 'color:#fff;font-size:24px';
                badge.appendChild(icon);
                large.appendChild(badge);
            }
            const small = el('div', 'small-image-container');
            const smallImgEl = el('img', 'small-image');
            smallImgEl.id = 'rpc-small-img';
            smallImgEl.alt = '';
            smallImgEl.onclick = () => editRpcElement('smallImage');
            smallImgEl.onerror = () => { small.style.display = 'none'; };
            if (smallImg) smallImgEl.src = smallImg; else small.style.display = 'none';
            small.appendChild(smallImgEl);
            images.append(large, small);

            const info = el('div', 'activity-details');
            const name = el('h4', 'activity-name', title || 'Activity Name');
            name.id = 'rpc-activity-name';
            name.onclick = () => editRpcElement('activityName');
            const detailsEl = el('p', 'activity-details-text', details);
            detailsEl.id = 'rpc-activity-details-text';
            detailsEl.onclick = () => editRpcElement('activityDetails');
            detailsEl.style.display = details ? '' : 'none';
            const stateEl = el('p', 'activity-state', state);
            stateEl.id = 'rpc-activity-state';
            stateEl.onclick = () => editRpcElement('activityState');
            stateEl.style.display = state ? '' : 'none';
            const ts = el('p', 'activity-timestamp', '00:00 elapsed');
            ts.id = 'rpc-timestamp';
            ts.style.display = timer ? '' : 'none';
            info.append(name, detailsEl, stateEl, ts);
            card.append(images, info);

            if (buttons.length) {
                const row = el('div', 'activity-buttons');
                buttons.slice(0, 2).forEach(b => {
                    const btn = el('button', 'activity-button', b.label);
                    btn.type = 'button';
                    btn.title = b.url || '';
                    row.appendChild(btn);
                });
                card.appendChild(row);
            }
        }
        function saveRpcConfig() {
            if (typeof window.pywebview === 'undefined' || !window.pywebview.api) return;
            const data = {};
            document.querySelectorAll('#rpc-fields input[type="text"]').forEach(i => { data[i.id.replace('rpc-input-','')] = i.value; });
            document.querySelectorAll('#rpc-fields select').forEach(s => { data[s.id.replace('rpc-input-','')] = s.value; });
            document.querySelectorAll('#rpc-fields input[type="checkbox"]').forEach(c => { data[c.id.replace('rpc-input-','')] = c.checked; });

            if (currentRpcType === 'rpc') {
                const buttons = [];
                for (let i = 0; i < 2; i++) {
                    const label = document.getElementById('rpc-btn-label-' + i);
                    const url = document.getElementById('rpc-btn-url-' + i);
                    if (label && url && (label.value || url.value)) {
                        buttons.push({label: label.value, url: url.value});
                    }
                }
                data.Buttons = buttons;

                if (data.Timer !== undefined) data.Timer = data.Timer === 'true' || data.Timer === true;
            }
            if (currentRpcType === 'spotify' && data.SongLength !== undefined) { data.SongLength = parseInt(data.SongLength) || 0; }
            window.pywebview.api.save_rpc_config(currentRpcType, JSON.stringify(data)).then(async () => {
                await config_edit('rpc', currentRpcType);
                const statusDot = document.getElementById('rpc-status-dot');
                const enableToggle = document.getElementById('rpc-enable-toggle');
                document.getElementById('rpc-status-text').innerText = 'Active: ' + currentRpcType;
                if (statusDot) statusDot.style.color = 'var(--accent)';
                if (enableToggle) enableToggle.checked = true;
                setQuickToggle('rpc', true);
                if (!(await applyRpc())) return;
                pywebview.api.sendnotif('Saved & applied RPC config: ' + currentRpcType);

                const saveBtn = document.querySelector('.rpc-btn.primary');
                if (saveBtn) {
                    saveBtn.classList.add('success');
                    setTimeout(() => {
                        saveBtn.classList.remove('success');
                    }, 800);
                }
            }).catch(e => console.error(e));
        }

        let allCommands = []; let cmdCategories = []; let activeCmdCategory = 'all';
        function loadCommands() {
            if (typeof window.pywebview === 'undefined' || !window.pywebview.api) return;
            const currentFilter = () => (document.getElementById('cmd-search') || {}).value || '';
            if (allCommands.length) { renderCommands(currentFilter()); return; }
            window.pywebview.api.get_commands_info().then(data => {
                allCommands = data || []; cmdCategories = ['all'];
                const cats = new Set();
                allCommands.forEach(c => { if(c.help) cats.add(c.help); });
                cats.forEach(c => cmdCategories.push(c));
                renderCommandCategories(); renderCommands(currentFilter());
            }).catch(e => console.error(e));
        }
        function renderCommandCategories() {
            const bar = document.getElementById('cmd-categories');
            bar.innerHTML = '';
            cmdCategories.forEach(c => {
                const div = document.createElement('div');
                div.className = 'cmd-category' + (c === activeCmdCategory ? ' active' : '');
                div.innerText = c === 'all' ? 'All' : c;
                div.onclick = () => { activeCmdCategory = c; renderCommandCategories(); renderCommands(); };
                bar.appendChild(div);
            });
        }
        function renderCommands(filter='') {
            const grid = document.getElementById('cmd-grid');
            grid.innerHTML = '';
            let cmds = allCommands;
            if (activeCmdCategory !== 'all') cmds = cmds.filter(c => c.help === activeCmdCategory);
            if (filter) cmds = cmds.filter(c => (c.name || '').toLowerCase().includes(filter.toLowerCase()) || (c.description && c.description.toLowerCase().includes(filter.toLowerCase())));
            let rendered = 0, failed = 0;
            cmds.forEach(c => {

                try {
                    const card = document.createElement('div');
                    card.className = 'cmd-card';
                    const header = document.createElement('div');
                    header.className = 'cmd-card-header';
                    header.innerHTML = '<span class="cmd-card-name">' + escapeHtml(String(c.name || '?')) + '</span><span class="cmd-card-cat">' + escapeHtml(String(c.help || 'none')) + '</span>';
                    const desc = document.createElement('div');
                    desc.className = 'cmd-card-desc';
                    desc.innerText = c.description || 'No description';
                    card.appendChild(header); card.appendChild(desc);
                    grid.appendChild(card);
                    rendered++;
                } catch (e) {
                    failed++;
                    console.error('Failed to render command card:', c, e);
                }
            });
            console.log(`Commands tab: rendered ${rendered}/${cmds.length} command(s)` + (failed ? ` (${failed} failed - see errors above)` : ''));
        }
        document.addEventListener('DOMContentLoaded', () => {
            const searchEl = document.getElementById('cmd-search');
            if (searchEl) searchEl.addEventListener('input', e => renderCommands(e.target.value));
        });

        const config_edit = (data, new_value) => pywebview.api.configedit(data, new_value);
        const config_get = (data) => pywebview.api.configget(data);

        function switchtoggled(element, data) {
            if (element.checked) config_edit(data, true);
            else config_edit(data, false);
            setQuickToggle(data, element.checked);
        }
        function settoggle(element, bool) { element.checked = Boolean(bool); }

        function setQuickToggle(key, value) {
            const el = document.querySelector(`input[data-quick="${key}"]`);
            if (el) el.checked = Boolean(value);
        }
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('input[data-quick]').forEach(input => {
                input.addEventListener('change', () => {
                    const key = input.dataset.quick;
                    if (key === 'rpc') { toggleRpcEnabled(input.checked); return; }
                    config_edit(key, input.checked);
                    const settingsToggle = document.querySelector(`#${key} .toggle-switch input`);
                    if (settingsToggle) settingsToggle.checked = input.checked;
                });
            });
        });

        async function loadSettings() {
            try {
                const cfg = await pywebview.api.get_all_settings();
                if (!cfg) return;

                const setField = (id, value) => {
                    const box = document.getElementById(id);
                    if (!box) return;
                    const field = box.querySelector('.character-count-container textarea');
                    if (field) field.value = value ?? '';
                };
                const setToggle = (id, value) => {
                    const box = document.getElementById(id);
                    if (!box) return;
                    const input = box.querySelector('.toggle-switch input');
                    if (input) settoggle(input, value);
                };

                setField('token', cfg.token);
                setField('prefix', cfg.prefix);
                setField('delete_timer', cfg.delete_timer);
                setField('afkmsg', cfg.afkmsg);
                setField('nitro_sniper_redeemer', cfg.nitro_sniper_redeemer);
                setField('giveaway_delay', cfg.giveaway_delay);
                setField('dmlogger_webhook_url', cfg.dmlogger_webhook_url);
                setField('nitro_webhook_url', cfg.nitro_webhook_url);
                setField('giveaway_webhook_url', cfg.giveaway_webhook_url);
                setField('pinglogger_webhook_url', cfg.pinglogger_webhook_url);
                setField('relationship_webhook_url', cfg.relationship_webhook_url);
                setField('error_webhook_url', cfg.error_webhook_url);
                ['music_whitelist', 'nitro_blacklist_ids', 'giveaway_bot_ids', 'giveaway_blacklist_ids']
                    .forEach(k => setField(k, (cfg[k] || []).join(', ')));
                setField('music_volume', cfg.music_volume ?? '');
                setToggle('music_autoplay', cfg.music_autoplay);

                setToggle('afkmode', cfg.afkmode);
                setToggle('nitro_sniper', cfg.nitro_sniper);
                setToggle('giveaway_sniper', cfg.giveaway_sniper);
                setToggle('pinglogger', cfg.pinglogger);
                setToggle('dmlogger', cfg.dmlogger);
                setToggle('sessionlogger', cfg.sessionlogger);
                setToggle('webhooknotifs', cfg.webhooknotifs);
                setToggle('relationshiplogger', cfg.relationshiplogger);
                setToggle('selfthrottle', cfg.selfthrottle);
                setToggle('autovcleave', cfg.autovcleave);
                setToggle('autobackup', cfg.autobackup);

                const embedDropdown = document.getElementById('EmbedDropdown');
                if (embedDropdown && cfg.embed_mode) embedDropdown.value = cfg.embed_mode;
                const deviceDropdown = document.getElementById('DeviceDropdown');
                if (deviceDropdown && cfg.device) deviceDropdown.value = cfg.device;

                ['afkmode', 'nitro_sniper', 'giveaway_sniper', 'selfthrottle', 'pinglogger', 'dmlogger'].forEach(k => setQuickToggle(k, cfg[k]));
                setQuickToggle('rpc', !!cfg.rpc);
                const prefix = cfg.prefix || '';
                const prefixEl = document.getElementById('ov-prefix');
                if (prefixEl) prefixEl.textContent = prefix;
                document.querySelectorAll('.ov-prefix-inline').forEach(el => { el.textContent = prefix; });
                const device = cfg.device || 'N/A';
                const deviceEl = document.getElementById('ov-device');
                if (deviceEl) deviceEl.textContent = device;
                const connSub = document.getElementById('conn-sub');
                if (connSub && cfg.device) connSub.textContent = `Gateway · ${cfg.device} device`;
            } catch (e) {
                console.error('Error loading settings:', e);
            }
        }
        document.addEventListener('DOMContentLoaded', () => loadSettings());

        function setLowGraphics(enabled) {
            document.body.classList.toggle('low-graphics', enabled);
            try { localStorage.setItem('lowGraphics', enabled ? '1' : '0'); } catch (e) {}
        }
        document.addEventListener('DOMContentLoaded', () => {
            const lgToggle = document.querySelector('#lowgraphics input[type="checkbox"]');
            if (lgToggle) lgToggle.checked = document.body.classList.contains('low-graphics');
        });
        function adjustDisplayPosition() {  }

        function resizeBadgeBox() {
            const bb = document.getElementById('badgebox');
            if (!bb) return;
            bb.style.width = 'auto';
        }
        function updateBadges(badges) {
            const bb = document.getElementById('badgebox');
            bb.innerHTML = '';
            if (badges && badges.length) {
                badges.forEach(b => {
                    const img = document.createElement('img');
                    img.src = b;
                    img.alt = 'Badge';
                    img.onerror = function() { this.style.display = 'none'; };
                    bb.appendChild(img);
                });
                bb.style.display = 'inline-flex';
                resizeBadgeBox();
            } else {
                bb.style.display = 'none';
            }
        }
        function fetchBadges() {
            if (typeof window.pywebview === 'undefined' || !window.pywebview.api) return;
            window.pywebview.api.get_badges().then(b => updateBadges(b));
        }

        function initializeApi() {
            return new Promise(resolve => {
                const iv = setInterval(() => { if(typeof pywebview!=='undefined'&&pywebview.api){ clearInterval(iv); resolve(); } }, 100);
            });
        }

        let themes = [];
        async function updateThemeDropdown() {
            await initializeApi();
            if (!themes.length) {
                try { themes = await pywebview.api.get_file_names(); populateDropdown(document.getElementById('CThemeDropdown')); }
                catch(e) { console.error(e); }
            }
        }
        function populateDropdown(dd) {
            dd.innerHTML = '';
            const o = document.createElement('option'); o.value=''; o.textContent='Repent'; dd.appendChild(o);
            themes.forEach(t => {
                const op = document.createElement('option'); op.value=t;
                op.textContent = t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
                dd.appendChild(op);
            });
            dd.value = localStorage.getItem('lastSelectedTheme') || '';
        }
        function handleDropdownChange(e) {
            const v = e.target.value;
            localStorage.setItem('lastSelectedTheme', v);
            config_edit('theme', v === '' ? '' : v);
            pywebview.api.terminal_ui();
            e.target.style.display='none'; e.target.offsetHeight; e.target.style.display='';
        }
        document.addEventListener('DOMContentLoaded', () => {
            initializeApi().then(() => {
                updateThemeDropdown();
                loadDiscordProfile();
                loadRpcConfig();
                const dd = document.getElementById('CThemeDropdown');
                dd.addEventListener('click', async function() { try { themes = await pywebview.api.get_file_names(); populateDropdown(this); } catch(e){console.error(e);} });
                dd.addEventListener('change', handleDropdownChange);
            });
        });

        function populateEThemeDropdown(dd) {
            dd.innerHTML = '';
            pywebview.api.get_etheme_names().then(ethemes => {
                ethemes.forEach(t => {
                    const o = document.createElement('option'); o.value=t;
                    o.textContent = t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
                    dd.appendChild(o);
                });
                dd.value = localStorage.getItem('lastSelectedETheme') || '';
            });
        }
        function setactive() {
            const v = document.getElementById('EThemeDropdown').value;
            config_edit('etheme', v);
            pywebview.api.sendnotif('Set Active Embed Theme To: ' + v);
        }
        function applyEmbedTheme(theme) {
            if (!theme) return;
            if (typeof setColor === 'function') setColor(theme.color);
            const imgField = document.querySelector('#EmbedImage .character-count-container textarea');
            if (imgField) imgField.value = theme.image;
            const imgPreview = document.getElementById('EMBEDIMGURL');
            if (imgPreview) {
                imgPreview.src = theme.image || '';
                imgPreview.style.display = theme.image ? 'block' : 'none';
            }
            const titleField = document.querySelector('#EmbedTitleUrl .character-count-container textarea');
            if (titleField) titleField.value = theme.title_url;
            const cmdField = document.querySelector('#EmbedCMDUrl .character-count-container textarea');
            if (cmdField) cmdField.value = theme.cmd_url;
            const providerEl = document.getElementById('EMBEDPROVIDER');
            if (providerEl) providerEl.textContent = 'example CMD';

            const authorNameField = document.querySelector('#EmbedAuthorName .character-count-container textarea');
            if (authorNameField) authorNameField.value = theme.author_name || '';
            const authorUrlField = document.querySelector('#EmbedAuthorUrl .character-count-container textarea');
            if (authorUrlField) authorUrlField.value = theme.author_url || '';
            const thumbnailField = document.querySelector('#EmbedThumbnail .character-count-container textarea');
            if (thumbnailField) thumbnailField.value = theme.thumbnail || '';
            const footerField = document.querySelector('#EmbedFooterText .character-count-container textarea');
            if (footerField) footerField.value = theme.footer_text || '';
            const timestampToggle = document.getElementById('EmbedShowTimestampToggle');
            if (timestampToggle) timestampToggle.checked = !!theme.show_timestamp;

            updateEmbedPreviewExtras();
        }

        function updateEmbedPreviewExtras() {
            const authorNameField = document.querySelector('#EmbedAuthorName .character-count-container textarea');
            const authorLine = document.getElementById('EMBEDAUTHORLINE');
            if (authorLine) {
                const name = authorNameField ? authorNameField.value : '';
                authorLine.textContent = name;
                authorLine.style.display = name ? 'block' : 'none';
            }
            const footerField = document.querySelector('#EmbedFooterText .character-count-container textarea');
            const timestampToggle = document.getElementById('EmbedShowTimestampToggle');
            const footerLine = document.getElementById('EMBEDFOOTERLINE');
            if (footerLine) {
                const footerText = footerField ? footerField.value : '';
                const showTs = timestampToggle ? timestampToggle.checked : false;
                let text = footerText;
                if (showTs) text = text ? `${text} • ${new Date().toLocaleString()}` : new Date().toLocaleString();
                footerLine.textContent = text;
                footerLine.style.display = text ? 'block' : 'none';
            }
        }
        document.addEventListener('DOMContentLoaded', () => {
            initializeApi().then(() => {
                pywebview.api.initialethemers().then(applyEmbedTheme);
                const dd = document.getElementById('EThemeDropdown');
                populateEThemeDropdown(dd);
                dd.addEventListener('change', function() { pywebview.api.setethemers(this.value).then(applyEmbedTheme); });
            });
        });

        function createetheme() {
            document.querySelector('.createthememodal').classList.add('visible');
            document.querySelector('.modalbg').classList.add('visible');
        }
        function closethememodal() {
            document.querySelector('.createthememodal').classList.remove('visible');
            document.querySelector('.modalbg').classList.remove('visible');
            document.getElementById('EmbedmodalInput').style.cssText = 'border-color: var(--border);';
            document.getElementById('EmbedmodalInput').placeholder = 'Embed Theme Name Here...';
        }
        function createnewetheme() {
            const name = document.getElementById('EmbedmodalInput').value;
            const dd = document.getElementById('EThemeDropdown');
            if (name === '') {
                document.getElementById('EmbedmodalInput').style.cssText = 'border-color: red;';
                document.getElementById('EmbedmodalInput').placeholder = 'Name cannot be empty...';
                return;
            }
            pywebview.api.createnewetheme(name).then(() => {
                localStorage.setItem('lastSelectedETheme', name);
                const op = document.createElement('option'); op.value=name;
                op.textContent = name.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                dd.appendChild(op); dd.value=name;
                closethememodal();
                pywebview.api.sendnotif('Created Embed Theme: ' + name);
            });
            pywebview.api.setethemers(name).then(applyEmbedTheme);
            document.getElementById('EmbedmodalInput').value = '';
        }
        function saveetheme() {
            const name = document.getElementById('EThemeDropdown').value;
            const color = pickr.getSelectedColor().toHEXA().toString();
            const tu = document.getElementById('EmbedTitleUrl').querySelector('textarea').value;
            const cu = document.getElementById('EmbedCMDUrl').querySelector('textarea').value;
            const img = document.getElementById('EmbedImage').querySelector('textarea').value;
            const authorName = document.getElementById('EmbedAuthorName').querySelector('textarea').value;
            const authorUrl = document.getElementById('EmbedAuthorUrl').querySelector('textarea').value;
            const thumbnail = document.getElementById('EmbedThumbnail').querySelector('textarea').value;
            const footerText = document.getElementById('EmbedFooterText').querySelector('textarea').value;
            const showTimestamp = document.getElementById('EmbedShowTimestampToggle').checked;
            pywebview.api.saveethemers(name, color, img, tu, cu, authorName, authorUrl, thumbnail, footerText, showTimestamp);
            pywebview.api.sendnotif('Saved Embed Theme: ' + name);
        }
        function updootembedimagee(e) { document.getElementById('EMBEDIMGURL').src = e.target.value; }
        function finishedittext(e) {
            const box = e.target.closest('.settingbox');
            const data = box.id;
            const kind = box.dataset.kind;
            let val = e.target.value;
            if (kind === 'idlist') {
                const parts = val.split(/[\s,]+/).filter(Boolean);
                const bad = parts.filter(p => !/^\d{15,20}$/.test(p));
                if (bad.length) {
                    showNotification('Not saved', `These aren't valid Discord IDs: ${escapeHtml(bad.join(', '))}`, 'warning');
                    return;
                }
                val = [...new Set(parts)];
                e.target.value = val.join(', ');
            } else if (kind === 'int') {
                if (val.trim() === '') return;
                const n = Number(val);
                if (!Number.isInteger(n) || n < 0 || n > 200) {
                    showNotification('Not saved', 'Enter a whole number from 0 to 200.', 'warning');
                    return;
                }
                val = n;
            } else if (data === 'giveaway_delay') {
                val = Number(val);
            }
            config_edit(data, val);
        }

        document.addEventListener('DOMContentLoaded', function() {

            const titleInput = document.getElementById('EmbedTitleUrl').querySelector('.character-count-container textarea');
            if (titleInput) {
                titleInput.addEventListener('input', function() {
                    document.getElementById('EMBEDTITLEURL').textContent = this.value || 'Example Title';
                });
            }

            const imageInput = document.getElementById('EmbedImage').querySelector('.character-count-container textarea');
            if (imageInput) {
                imageInput.addEventListener('blur', function() {
                    const img = document.getElementById('EMBEDIMGURL');
                    if (this.value) {
                        img.src = this.value;
                        img.style.display = 'block';
                    } else {
                        img.style.display = 'none';
                    }
                });
            }

            const cmdInput = document.getElementById('EmbedCMDUrl').querySelector('.character-count-container textarea');
            if (cmdInput) {
                cmdInput.addEventListener('input', function() {
                    document.getElementById('EMBEDPROVIDER').textContent = 'example CMD';
                });
            }

            document.getElementById('EMBEDPROVIDER').addEventListener('click', function() {
                const v = document.getElementById('EmbedCMDUrl').querySelector('textarea').value;
                if (v) pywebview.api.open_link(v);
            });

            document.getElementById('EMBEDTITLEURL').addEventListener('click', function() {
                const v = document.getElementById('EmbedTitleUrl').querySelector('textarea').value;
                if (v) pywebview.api.open_link(v);
            });

            const authorNameInput = document.getElementById('EmbedAuthorName').querySelector('.character-count-container textarea');
            if (authorNameInput) authorNameInput.addEventListener('input', updateEmbedPreviewExtras);
            const footerInput = document.getElementById('EmbedFooterText').querySelector('.character-count-container textarea');
            if (footerInput) footerInput.addEventListener('input', updateEmbedPreviewExtras);
            const timestampToggle = document.getElementById('EmbedShowTimestampToggle');
            if (timestampToggle) timestampToggle.addEventListener('change', updateEmbedPreviewExtras);
        });

        function populateGuildThemeDropdowns() {
            const guildDD = document.getElementById('GuildThemeGuildDropdown');
            const themeDD = document.getElementById('GuildThemeThemeDropdown');
            if (!guildDD || !themeDD) return;
            pywebview.api.get_guild_list().then(guilds => {
                guildDD.innerHTML = '';
                guilds.forEach(g => {
                    const o = document.createElement('option'); o.value = g.id;
                    o.textContent = g.name.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    guildDD.appendChild(o);
                });
            });
            pywebview.api.get_etheme_names().then(themes => {
                themeDD.innerHTML = '';
                themes.forEach(t => {
                    const o = document.createElement('option'); o.value = t;
                    o.textContent = t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    themeDD.appendChild(o);
                });
            });
        }
        function refreshGuildThemeList() {
            const list = document.getElementById('GuildThemeList');
            if (!list) return;
            Promise.all([pywebview.api.get_guild_theme_overrides(), pywebview.api.get_guild_list()]).then(([overrides, guilds]) => {
                const nameById = {};
                guilds.forEach(g => { nameById[g.id] = g.name; });
                const entries = Object.entries(overrides);
                if (entries.length === 0) {
                    list.textContent = 'No servers have a theme override - all use the active global theme.';
                    return;
                }
                list.innerHTML = entries.map(([gid, theme]) => {
                    const gname = (nameById[gid] || gid).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    return `<div>${gname} → ${theme.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</div>`;
                }).join('');
            });
        }
        function setGuildTheme() {
            const guildDD = document.getElementById('GuildThemeGuildDropdown');
            const themeDD = document.getElementById('GuildThemeThemeDropdown');
            if (!guildDD.value || !themeDD.value) return;
            pywebview.api.set_guild_theme_override(guildDD.value, themeDD.value).then(() => {
                pywebview.api.sendnotif(`Pinned "${themeDD.value}" theme to that server`);
                refreshGuildThemeList();
            });
        }
        function clearGuildTheme() {
            const guildDD = document.getElementById('GuildThemeGuildDropdown');
            if (!guildDD.value) return;
            pywebview.api.clear_guild_theme_override(guildDD.value).then(() => {
                pywebview.api.sendnotif('Cleared that server\'s theme override');
                refreshGuildThemeList();
            });
        }
        document.addEventListener('DOMContentLoaded', () => {
            initializeApi().then(() => {
                populateGuildThemeDropdowns();
                refreshGuildThemeList();
            });
        });
        document.querySelectorAll('.no-newline').forEach(ta => ta.addEventListener('blur', finishedittext));
        document.querySelectorAll('.no-newline, .no-newline-embed').forEach(ta => {
            ta.addEventListener('keydown', function(e) { if (e.key === 'Enter') e.preventDefault(); });
        });
        document.getElementById('DeviceDropdown').addEventListener('click', e => e.stopPropagation());
        document.getElementById('CThemeDropdown').addEventListener('click', e => e.stopPropagation());
        document.getElementById('EmbedDropdown').addEventListener('click', e => e.stopPropagation());

        function showNotification(title, body = '', type = 'info', duration = 4000) {
            const container = document.getElementById('notification-container');
            const notif = document.createElement('div');
            notif.className = `notification ${type}`;
            notif.style.position = 'relative';

            const icons = {
                success: 'fa-circle-check',
                warning: 'fa-triangle-exclamation',
                error: 'fa-circle-xmark',
                info: 'fa-circle-info'
            };

            notif.innerHTML = `
                <button class="notification-close" onclick="this.parentElement.classList.add('removing'); setTimeout(() => this.parentElement.remove(), 300)"><i class="fa-solid fa-xmark"></i></button>
                <div class="notification-header"><i class="fa-solid ${icons[type]}"></i><span class="notification-title">${title}</span></div>
                ${body ? `<div class="notification-body">${body}</div>` : ''}
            `;

            notif.onclick = (e) => {
                if (!e.target.closest('.notification-close')) {
                    notif.classList.add('removing');
                    setTimeout(() => notif.remove(), 300);
                }
            };

            container.appendChild(notif);

            if (duration > 0) {
                setTimeout(() => {
                    if (notif.parentElement) {
                        notif.classList.add('removing');
                        setTimeout(() => notif.remove(), 300);
                    }
                }, duration);
            }
        }

        const ansiColorMap = {
            '30':'color:#000','31':'color:red','32':'color:green','33':'color:yellow','34':'color:blue','35':'color:magenta','36':'color:cyan','37':'color:white',
            '90':'color:rgb(83,84,81)','91':'color:rgb(247,84,81)','92':'color:rgb(82,255,81)','93':'color:rgb(248,255,82)','94':'color:rgb(81,84,245)','95':'color:rgb(239,84,254)','96':'color:rgb(84,255,237)','97':'color:white',
            '40':'background-color:#000','41':'background-color:red','42':'background-color:green','43':'background-color:yellow','44':'background-color:blue','45':'background-color:magenta','46':'background-color:cyan','47':'background-color:white',
            '100':'background-color:rgb(128,128,128)','101':'background-color:rgb(255,102,102)','102':'background-color:rgb(144,238,144)','103':'background-color:rgb(255,255,102)','104':'background-color:rgb(102,178,255)','105':'background-color:rgb(255,140,210)','106':'background-color:rgb(102,255,255)','107':'background-color:white',
            '1':'font-weight:bold','22':'font-weight:normal','39':'color:inherit','49':'background-color:inherit'
        };
        function parseAnsiColors(text) {
            return text.replace(/\x1b\[(\d{1,2}(;\d{1,2})*)m/g, (match, codes) => {
                const styles = codes.split(';').map(c => ansiColorMap[c] || '').filter(Boolean).join('; ');
                return styles ? '</span><span style="' + styles + ';">' : '</span>';
            });
        }
        function parseHexColors(text) {
            return text.replace(/\{#([A-Fa-f0-9]{6})\}/g, (m, hex) => '</span><span style="color:#'+hex+';background:transparent;">').replace(/\}/g, '</span>');
        }
        function escapeHtml(unsafe) { return unsafe.replace(/[&<"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])); }
        const OV_LOG_MAX = 6;
        function mirrorToOverview(html) {
            const log = document.getElementById('ov-log');
            if (!log) return;
            const line = document.createElement('div');
            line.innerHTML = '<span>' + html + '</span>';
            if (!line.textContent.trim()) return;
            log.appendChild(line);
            while (log.children.length > OV_LOG_MAX) log.removeChild(log.firstChild);
        }
        function print(message, mirror = true) {
            try {
                let msg = escapeHtml(message); msg = parseAnsiColors(msg); msg = parseHexColors(msg);
                const regex = /\[(.*?)\]\((https?:\/\/|discord:\/\/)(.*?)\)/g;
                let final = '', match, prev = 0;
                while ((match = regex.exec(msg)) !== null) {
                    const url = match[2] + match[3];
                    const btn = '<button style="color:rgb(255,84,81);background:transparent;border:none;cursor:pointer;font-family:Consolas,sans-serif;font-size:13px;" onclick="pywebview.api.open_link(\''+url+'\')">'+match[1]+'</button>';
                    final += msg.slice(prev, match.index) + btn;
                    prev = match.index + match[0].length;
                }
                final += msg.slice(prev);
                const el = document.getElementById('app-console');
                el.insertAdjacentHTML('beforeend', '<div class="console-message">' + final + '</div>');
                el.scrollTop = el.scrollHeight;
                if (mirror) mirrorToOverview(final);
            } catch(e) { console.error(e); }
        }
        function printCenter(message) {
            const el = document.getElementById('app-console');
            const line = document.createElement('div'); line.classList.add('line');
            line.innerHTML = parseAnsiColors(message.replace(/\n/g, '<br>'));
            el.appendChild(line); el.scrollTop = el.scrollHeight;
        }
        function cls() { const el = document.getElementById('app-console'); if(el) el.innerHTML = ''; }
        function printmax(ch) { const el = document.getElementById('app-console'); if(!el)return; const r = Math.floor(el.clientWidth/10); print(ch.repeat(r), false); }
        function printascii(ascii) { try { ascii.split('\n').forEach(l => print(l, false)); } catch(e){console.error(e);} }

        let consoleSince = 0;
        async function pollConsole() {
            try {
                const resp = await fetch(`/api/console?since=${consoleSince}`);
                const data = await resp.json();
                if (data && data.entries && data.entries.length) {
                    data.entries.forEach(entry => {
                        consoleSince = entry.id;
                        switch (entry.kind) {
                            case 'cls': cls(); break;
                            case 'printcenter': printCenter(entry.text); break;
                            case 'printmax': printmax(entry.text); break;
                            case 'printascii': printascii(entry.text); break;
                            default: print(entry.text);
                        }
                    });
                } else if (data && typeof data.latest === 'number') {
                    consoleSince = data.latest;
                }
            } catch (e) {  }
            setTimeout(pollConsole, 700);
        }
        document.addEventListener('DOMContentLoaded', () => pollConsole());

        function updateProgressBars(fv, gv) {
            const friendPct = Math.round((fv/1000)*100);
            const guildPct = Math.round((gv/100)*100);
            document.getElementById('friendbar').style.width = friendPct + '%';
            document.getElementById('guildbar').style.width = guildPct + '%';
            const fn2 = document.getElementById('friendnum2'), gn2 = document.getElementById('guildnum2');
            if(fn2) fn2.innerText = fv; if(gn2) gn2.innerText = gv;
        }

        const embedElement = document.querySelector('.embedpreview');
        const pickr = Pickr.create({
            el: '.color-picker', theme: 'nano',
            components: { hue: true, interaction: { hex: false, input: true } }, background: '#111115'
        });
        pickr.on('change', (color) => {
            pickr.applyColor(color);
            if(embedElement) embedElement.style.borderLeftColor = color.toHEXA().toString();
        });
        function setColor(hex) {
            hex = hex.startsWith('#') ? hex.slice(1) : hex;
            if(!/^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex)) return;
            pickr.setColor('#'+hex);
            if(embedElement) embedElement.style.borderLeftColor = '#'+hex;
            pickr.applyColor();
        }

        let rpcStartTime = Date.now();
        let currentEditType = null;

        const elementTitles = {
            username: 'Edit Username',
            activityName: 'Edit Activity Name',
            activityState: 'Edit State',
            activityDetails: 'Edit Details',
            avatar: 'Edit Avatar URL',
            banner: 'Edit Banner (URL or Hex)',
            largeImage: 'Edit Large Image URL',
            smallImage: 'Edit Small Image URL'
        };

        const elementPlaceholders = {
            username: 'Enter username',
            activityName: 'Enter activity name',
            activityState: 'Enter state',
            activityDetails: 'Enter details',
            avatar: 'Enter avatar URL',
            banner: 'Enter banner URL or hex color',
            largeImage: 'Enter large image URL',
            smallImage: 'Enter small image URL'
        };

        const RPC_FIELD_FOR = {
            activityName: ['Title', 'SongTitle'],
            activityDetails: ['Description', 'ArtistName'],
            activityState: ['SubText', 'AlbumName'],
            largeImage: ['Large_Image', 'Image'],
            smallImage: ['Small_Image'],
        };
        function rpcFormInput(elementType) {
            return (RPC_FIELD_FOR[elementType] || []).map(k => document.getElementById('rpc-input-' + k)).find(Boolean) || null;
        }

        function editRpcElement(elementType) {
            currentEditType = elementType;
            const formInput = rpcFormInput(elementType);
            let currentValue = '';
            if (formInput) {
                currentValue = formInput.value;
            } else if (elementType === 'username') {
                currentValue = document.getElementById('rpc-username').textContent;
            } else if (elementType === 'avatar') {
                currentValue = document.getElementById('rpc-avatar').src || '';
            }

            document.getElementById('rpc-edit-modal-title').textContent = elementTitles[elementType];
            document.getElementById('rpc-edit-modal-input').placeholder = elementPlaceholders[elementType];
            document.getElementById('rpc-edit-modal-input').value = currentValue;

            document.getElementById('rpc-edit-modal-bg').classList.add('visible');
            document.getElementById('rpc-edit-modal-input').focus();
        }

        function closeRpcEditModal() {
            document.getElementById('rpc-edit-modal-bg').classList.remove('visible');
            currentEditType = null;
        }

        function saveRpcEditModal() {
            const newValue = document.getElementById('rpc-edit-modal-input').value;
            if (currentEditType) {
                updateRpcElement(currentEditType, newValue);
            }
            closeRpcEditModal();
        }

        function updateRpcElement(elementType, value) {
            const formInput = rpcFormInput(elementType);
            if (formInput) {
                formInput.value = value;
                updateRpcPreview(getCurrentRpcData(), currentRpcType);
                return;
            }
            switch(elementType) {
                case 'username':
                    document.getElementById('rpc-username').textContent = value || 'Username';
                    break;
                case 'avatar':
                    if (value) {
                        document.getElementById('rpc-avatar').src = value;
                        document.getElementById('rpc-avatar').style.display = 'block';
                    } else {
                        document.getElementById('rpc-avatar').style.display = 'none';
                    }
                    break;
                case 'banner':
                    if (value.startsWith('#')) {
                        document.getElementById('rpc-banner').style.background = value;
                    } else if (/^https?:\/\//.test(value)) {
                        document.getElementById('rpc-banner').style.background = `url("${encodeURI(value)}") center/cover`;
                    }
                    break;
            }
        }

        setInterval(() => {
            const elapsed = Math.floor((Date.now() - rpcStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            const ts = document.getElementById('rpc-timestamp');
            if (ts) ts.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')} elapsed`;
        }, 1000);

        function snowflakeToDate(id) {
            const snowflake = BigInt(id);
            const epoch = BigInt('1420070400000');
            const timestamp = Number((snowflake >> 22n) + epoch);
            return new Date(timestamp);
        }

        function formatDate(date) {
            const options = { year: 'numeric', month: 'long' };
            return date.toLocaleDateString('en-US', options);
        }

        async function loadDiscordProfile(retriesLeft = 3) {
            try {
                const profile = await pywebview.api.get_user_profile();
                if (!profile) {
                    if (retriesLeft > 0) {
                        setTimeout(() => loadDiscordProfile(retriesLeft - 1), 1000);
                    } else {
                        console.warn('Repent: could not load Discord profile after retries, leaving placeholders.');
                    }
                    return;
                }

                const statusDot = document.getElementById('page-header-dot');
                const statusText = document.getElementById('page-header-status-text');
                if (statusDot && statusText) {
                    statusDot.classList.add('connected');
                    if (profile.global_name) {
                        statusText.textContent = `Connected as ${profile.global_name}`;
                    } else if (profile.username) {
                        statusText.textContent = `Connected as ${profile.username}`;
                    }
                }

                const welcomeUsernameEl = document.getElementById('welcome-username');
                if (welcomeUsernameEl) {
                    if (profile.global_name) {
                        welcomeUsernameEl.textContent = profile.global_name;
                    } else if (profile.username) {
                        welcomeUsernameEl.textContent = profile.username;
                    }
                }

                const globalUsernameEl = document.getElementById('global-username');
                if (globalUsernameEl) {
                    if (profile.global_name) {
                        globalUsernameEl.textContent = profile.global_name;
                    } else if (profile.username) {
                        globalUsernameEl.textContent = profile.username;
                    }
                }

                const userTagEl = document.getElementById('user-tag');
                if (userTagEl && profile.username) {
                    userTagEl.textContent = profile.username + (profile.discriminator && profile.discriminator !== '0' ? '#' + profile.discriminator : '');
                }

                const rpcUserTagEl = document.getElementById('rpc-user-tag');
                if (rpcUserTagEl && profile.username) {
                    rpcUserTagEl.textContent = profile.username + (profile.discriminator && profile.discriminator !== '0' ? '#' + profile.discriminator : '');
                }

                const userIdEl = document.getElementById('user-id');
                if (userIdEl && profile.id) {
                    userIdEl.textContent = profile.id;
                }

                const memberSinceEl = document.getElementById('rpc-member-since');
                if (memberSinceEl && profile.id) {
                    const creationDate = snowflakeToDate(profile.id);
                    memberSinceEl.textContent = formatDate(creationDate);
                }

                if (profile.avatar) {
                    const avatarUrl = `https://cdn.discordapp.com/avatars/${profile.id}/${profile.avatar}.png?size=256`;
                    const pfpEl = document.getElementById('pfp');
                    if (pfpEl) {
                        pfpEl.src = avatarUrl;
                    }
                    const welcomeAvatarEl = document.getElementById('welcome-avatar');
                    if (welcomeAvatarEl) {
                        welcomeAvatarEl.src = avatarUrl;
                    }
                    document.getElementById('rpc-avatar').src = avatarUrl;
                    document.getElementById('rpc-avatar').style.display = 'block';
                }

                const accountBannerEl = document.getElementById('account-banner');
                if (accountBannerEl) {
                    if (profile.banner) {
                        const bannerUrl = `https://cdn.discordapp.com/banners/${profile.id}/${profile.banner}.png?size=1024`;
                        accountBannerEl.style.background = 'none';
                        accountBannerEl.style.backgroundImage = `url(${bannerUrl})`;
                        accountBannerEl.style.backgroundSize = 'cover';
                        accountBannerEl.style.backgroundPosition = 'center';
                        const rpcBannerEl = document.getElementById('rpc-banner');
                        rpcBannerEl.style.background = 'none';
                        rpcBannerEl.style.backgroundImage = `url(${bannerUrl})`;
                        rpcBannerEl.style.backgroundSize = 'cover';
                        rpcBannerEl.style.backgroundPosition = 'center';
                    } else if (profile.banner_color) {
                        accountBannerEl.style.backgroundImage = 'none';
                        accountBannerEl.style.background = profile.banner_color;
                        const rpcBannerEl = document.getElementById('rpc-banner');
                        rpcBannerEl.style.backgroundImage = 'none';
                        rpcBannerEl.style.background = profile.banner_color;
                    }
                }

                const bioBoxEl = document.getElementById('biobox');
                if (bioBoxEl && profile.bio) {
                    bioBoxEl.textContent = profile.bio;
                }

                let displayUsername = '';
                if (profile.global_name) {
                    displayUsername = profile.global_name;
                } else if (profile.username) {
                    displayUsername = profile.username;
                }
                if (displayUsername) {
                    document.getElementById('rpc-username').textContent = displayUsername;
                }

                if (profile.clan && profile.clan.tag) {
                    const clanTagEl = document.getElementById('rpc-clan-tag');
                    clanTagEl.textContent = profile.clan.tag;
                    clanTagEl.style.display = 'inline-block';
                }

                if (profile.bio) {
                    document.getElementById('rpc-bio').textContent = profile.bio;
                    const bioLabel = document.getElementById('rpc-bio-label');
                    if (bioLabel) bioLabel.style.display = 'block';
                }

                if (profile.badges && profile.badges.length > 0) {
                    const badgesEl = document.getElementById('rpc-badges');
                    badgesEl.innerHTML = '';
                    badgesEl.style.display = 'inline-flex';
                    profile.badges.forEach(badgeUrl => {
                        const img = document.createElement('img');
                        img.src = badgeUrl;
                        img.style.width = '18px';
                        img.style.height = '18px';
                        img.style.objectFit = 'contain';
                        img.style.borderRadius = '4px';
                        badgesEl.appendChild(img);
                    });
                }
                fetchBadges();

                const friendEl = document.getElementById('friendnum');
                if (friendEl) friendEl.textContent = profile.friend_count ?? 0;
                const guildEl = document.getElementById('guildnum');
                if (guildEl) guildEl.textContent = profile.guild_count ?? 0;
                const createdEl = document.getElementById('created-date');
                if (createdEl && profile.id) createdEl.textContent = formatDate(snowflakeToDate(profile.id));

                const setInfo = (id, value, fallback = 'N/A') => {
                    const el = document.getElementById(id);
                    if (el) el.textContent = (value === undefined || value === null || value === '') ? fallback : value;
                };
                const setPill = (id, isOn, onText, offText) => {
                    const el = document.getElementById(id);
                    if (!el) return;
                    el.textContent = isOn ? onText : offText;
                    el.classList.toggle('acc-pill-on', !!isOn);
                };
                setInfo('user-email', profile.email, 'Not linked');
                setInfo('user-phone', profile.phone, 'Not linked');
                setInfo('user-token', profile.token);
                setPill('user-nitro', profile.nitro, 'Yes', 'No');
                setPill('user-nsfw', profile.nsfw_allowed, 'Yes', 'No');
                setPill('user-mfa', profile.mfa_enabled, 'Enabled', 'Disabled');
                setInfo('user-lang', profile.locale);

                applyBotStats({
                    uptime_seconds: profile.bot_uptime_seconds,
                    latency_ms: profile.bot_latency_ms,
                    cmdcount: profile.bot_cmdcount,
                    version: profile.bot_version,
                });
            } catch (e) {
                console.error('Error loading Discord profile:', e);
                if (retriesLeft > 0) {
                    setTimeout(() => loadDiscordProfile(retriesLeft - 1), 1000);
                }
            }
        }

        let uptimeBase = null;
        function applyBotStats(stats) {
            if (!stats) return;
            const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
            if (typeof stats.uptime_seconds === 'number') {
                uptimeBase = { seconds: stats.uptime_seconds, at: Date.now() };
                setText('bot-uptime', formatUptime(stats.uptime_seconds));
            }
            setText('bot-latency', typeof stats.latency_ms === 'number' ? `${stats.latency_ms} ms` : 'N/A');
            if (typeof stats.cmdcount === 'number') {
                setText('bot-cmdcount', stats.cmdcount);
                setText('ov-cmd-total', stats.cmdcount || '');
            }
            if (stats.version) {
                setText('bot-version', stats.version);
                setText('sidebar-version', `v${stats.version} · selfbot`);
            }
        }
        async function refreshBotStats() {
            try { applyBotStats(await pywebview.api.get_bot_stats()); } catch (e) { }
        }
        setInterval(() => {
            if (!uptimeBase) return;
            const el = document.getElementById('bot-uptime');
            if (el) el.textContent = formatUptime(uptimeBase.seconds + Math.floor((Date.now() - uptimeBase.at) / 1000));
        }, 1000);
        document.addEventListener('DOMContentLoaded', () => {
            initializeApi().then(() => {
                refreshBotStats();
                setInterval(refreshBotStats, 5000);
            });
        });

        function formatUptime(seconds) {
            if (seconds === undefined || seconds === null || seconds < 0) return 'N/A';
            const days = Math.floor(seconds / 86400);
            const hours = Math.floor((seconds % 86400) / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            if (days > 0) return `${days}d ${hours}h ${minutes}m`;
            if (hours > 0) return `${hours}h ${minutes}m ${secs}s`;
            return `${minutes}m ${secs}s`;
        }

        document.addEventListener('DOMContentLoaded', () => {
            loadDiscordProfile();

            document.getElementById('rpc-edit-modal-bg').addEventListener('click', (e) => {
                if (e.target.id === 'rpc-edit-modal-bg') {
                    closeRpcEditModal();
                }
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeRpcEditModal();
                }
            });

            document.getElementById('rpc-edit-modal-input').addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    saveRpcEditModal();
                }
            });
        });

        window.addEventListener('resize', resizeBadgeBox);
window.addEventListener('resize', adjustDisplayPosition);

function openCommandSearch() {
    goPage('commands');
    const search = document.getElementById('cmd-search');
    if (search) { search.focus(); search.select(); }
}

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openCommandSearch();
        return;
    }
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const t = e.target;
    const typing = t && (t.isContentEditable || ['TEXTAREA', 'SELECT'].includes(t.tagName)
        || (t.tagName === 'INPUT' && !['checkbox', 'radio', 'button'].includes(t.type)));
    if (typing) return;
    const pages = { '1': 'account', '2': 'console', '3': 'rpc', '4': 'commands', ',': 'config' };
    if (pages[e.key]) goPage(pages[e.key]);
});

function formatClock(seconds) {
    if (!seconds && seconds !== 0) return '?';
    seconds = Math.max(0, Math.floor(seconds));
    const h = Math.floor(seconds / 3600), m = Math.floor((seconds % 3600) / 60), s = seconds % 60;
    return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0');
}

async function refreshMusicTile() {
    const tile = document.getElementById('ov-music');
    if (!tile || !document.getElementById('account').classList.contains('active')) return;
    let state = null;
    try { state = await pywebview.api.get_music_state(); } catch (e) { return; }
    const title = document.getElementById('ov-music-title');
    const sub = document.getElementById('ov-music-sub');
    const vc = document.getElementById('ov-music-vc');
    if (!state) {
        tile.classList.add('idle');
        title.textContent = 'Nothing playing';
        sub.textContent = '';
        sub.append('use ', Object.assign(document.createElement('span'), { className: 'ov-prefix-inline', textContent: (document.getElementById('ov-prefix') || {}).textContent || '' }), 'mplay in a voice channel');
        vc.textContent = '';
        return;
    }
    tile.classList.remove('idle');
    title.textContent = state.title || 'Unknown track';
    sub.textContent = state.guild ? `in ${state.guild}` : 'via ytqueue';
    vc.textContent = state.channel ? `vc #${state.channel}` : '';
    const pct = state.duration ? Math.min(100, (state.elapsed / state.duration) * 100) : 0;
    document.getElementById('ov-music-bar').style.width = pct + '%';
    document.getElementById('ov-music-time').textContent = `${formatClock(state.elapsed)} / ${state.duration ? formatClock(state.duration) : 'live'}`;
    document.getElementById('ov-music-queue').textContent = `${state.queued} queued · loop ${state.loop ? 'on' : 'off'}`;
}
document.addEventListener('DOMContentLoaded', () => {
    initializeApi().then(() => {
        refreshMusicTile();
        setInterval(refreshMusicTile, 3000);
    });
});

window.__repentReady = true;
window.dispatchEvent(new Event('repent:ready'));

document.addEventListener('DOMContentLoaded', () => {
    const POLL_MS = 500;
    const MAX_WAIT_MS = 30000;
    const SLOW_MS = 12000;
    const startTime = Date.now();
    const STAGES = [
        { key: 'Starting up', label: 'Starting up' },
        { key: 'Logging into Discord', label: 'Logging into Discord' },
        { key: 'Connected to Discord, syncing account data', label: 'Syncing account data' },
        { key: 'Building terminal and loading commands', label: 'Loading commands' },
    ];
    const reached = {};
    let current = 0;
    let revealed = false;

    const stageEl = document.getElementById('boot-stage');
    const fillEl = document.getElementById('boot-fill');
    const stepsEl = document.getElementById('boot-steps');
    const elapsedEl = document.getElementById('boot-elapsed');
    const hintEl = document.getElementById('boot-hint');
    const secs = ms => (ms / 1000).toFixed(1) + 's';

    stepsEl.innerHTML = STAGES.map(s => `<li><span>${s.label}</span><time></time></li>`).join('');
    reached[0] = 0;

    function render(headline, done) {
        stepsEl.querySelectorAll('li').forEach((li, i) => {
            li.className = done || i < current ? 'done' : i === current ? 'on' : '';
            const next = reached[i + 1] ?? (done ? reached.ready : undefined);
            li.querySelector('time').textContent = (done || i < current) && next !== undefined ? secs(next - reached[i]) : '';
        });
        fillEl.style.width = done ? '100%' : Math.max(4, (current / STAGES.length) * 100) + '%';
        if (stageEl.textContent !== headline) {
            stageEl.textContent = headline;
            stageEl.classList.remove('swap');
            void stageEl.offsetWidth;
            stageEl.classList.add('swap');
        }
    }

    const clock = setInterval(() => {
        const ms = Date.now() - startTime;
        const s = Math.floor(ms / 1000);
        elapsedEl.textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0');
        if (ms > SLOW_MS && !revealed) hintEl.textContent = 'Taking longer than usual. Check the terminal window for errors.';
    }, 250);

    function reveal(timedOut) {
        if (revealed) return;
        revealed = true;
        clearInterval(clock);
        if (timedOut) {
            console.warn('Repent: timed out waiting for the bot to connect, loading site anyway.');
        } else {
            reached.ready = Date.now() - startTime;
            render('Ready', true);
        }
        loadDiscordProfile();
        setTimeout(() => document.body.classList.add('loaded'), timedOut ? 0 : 450);
        setInterval(loadDiscordProfile, 30000);
    }

    function onStage(stage) {
        const idx = STAGES.findIndex(s => s.key === stage);
        if (idx > current) {
            for (let i = current + 1; i <= idx; i++) if (reached[i] === undefined) reached[i] = Date.now() - startTime;
            current = idx;
        }
        render(idx >= 0 ? STAGES[idx].label : (stage || 'Connecting to Discord'), false);
    }

    function pollStatus() {
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                if (data && data.ready) return reveal(false);
                if (Date.now() - startTime > MAX_WAIT_MS) return reveal(true);
                onStage(data && data.stage);
                setTimeout(pollStatus, POLL_MS);
            })
            .catch(() => {
                if (Date.now() - startTime > MAX_WAIT_MS) return reveal(true);
                setTimeout(pollStatus, POLL_MS);
            });
    }

    render(STAGES[0].label, false);
    pollStatus();
});
