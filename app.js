const $ = id => document.getElementById(id);
let songs = [], currentId = null, view = 'all', repeatMode = 0;
let searchTimer, progressTimer, ytPlayer = null, ytReady = false;

const formatTime = value => {
  const seconds = Number(value);
  if (!Number.isFinite(seconds)) return '00:00';
  return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
};
const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.message || 'Không thể kết nối với Python.');
  return data;
}
function notify(message) {
  $('status').textContent = message || 'Sẵn sàng';
  clearTimeout(notify.timer);
  notify.timer = setTimeout(() => $('status').textContent = 'Sẵn sàng', 2600);
}

window.onYouTubeIframeAPIReady = function () {
  ytPlayer = new YT.Player('youtubePlayer', {
    width: '356', height: '200', videoId: '',
    playerVars: {playsinline: 1, rel: 0},
    events: {
      onReady: () => { ytReady = true; ytPlayer.setVolume(80); },
      onStateChange: onPlayerStateChange,
      onError: () => notify('Video không phát được hoặc đã tắt tính năng nhúng.')
    }
  });
};

function onPlayerStateChange(event) {
  if (event.data === YT.PlayerState.PLAYING) {
    $('play').textContent = '❚❚'; startProgress();
    const duration = ytPlayer.getDuration();
    if (currentId && duration) updateDuration(duration);
  } else { $('play').textContent = '▶'; stopProgress(); }
  if (event.data === YT.PlayerState.ENDED) {
    if (repeatMode === 2) ytPlayer.playVideo();
    else if (repeatMode === 1 || getCurrent() !== songs.at(-1)) move('next');
  }
  render();
}
function startProgress() {
  stopProgress();
  progressTimer = setInterval(() => {
    if (!ytReady) return;
    const current = ytPlayer.getCurrentTime() || 0, duration = ytPlayer.getDuration() || 0;
    $('time').textContent = formatTime(current); $('duration').textContent = formatTime(duration);
    $('progress').value = duration ? current / duration * 100 : 0;
  }, 500);
}
function stopProgress() { clearInterval(progressTimer); }
async function updateDuration(duration) {
  const song = getCurrent();
  if (!song || Math.abs(Number(song.duration) - duration) < 1) return;
  song.duration = duration;
  try { await api(`/api/songs/${song.id}/duration`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({duration})}); }
  catch (_) {}
}

async function loadSongs() {
  const query = new URLSearchParams();
  if ($('search').value.trim()) query.set('q', $('search').value.trim());
  if (view === 'favorites') query.set('favorites', '1');
  try { const data = await api(`/api/songs?${query}`); songs = data.songs; currentId = data.current_id; render(); }
  catch (error) { notify(error.message); }
}
function render() {
  $('songList').innerHTML = songs.map((song, index) => `
    <article class="song ${song.id === currentId ? 'active' : ''}" data-id="${song.id}">
      <button class="row-play" title="Phát">${song.id === currentId && ytReady && ytPlayer.getPlayerState() === 1 ? '❚❚' : index + 1}</button>
      <div class="song-name"><img src="${song.thumbnail}" alt=""><strong>${escapeHtml(song.title)}</strong></div>
      <span>${escapeHtml(song.artist)}</span><span>${formatTime(song.duration)}</span>
      <div class="row-actions"><button data-action="favorite" class="${song.favorite ? 'liked' : ''}">${song.favorite ? '♥' : '♡'}</button><button data-action="delete">×</button></div>
    </article>`).join('');
  $('empty').hidden = songs.length > 0; $('count').textContent = songs.length;
  $('total').textContent = formatTime(songs.reduce((sum, song) => sum + Number(song.duration || 0), 0));
  $('headingTitle').textContent = view === 'favorites' ? 'Bài hát yêu thích' : 'Danh sách bài hát';
  updatePlayerInfo();
}
function getCurrent() { return songs.find(song => song.id === currentId); }
function updatePlayerInfo() {
  const song = getCurrent();
  $('currentTitle').textContent = song?.title || 'Chưa chọn bài hát'; $('currentArtist').textContent = song?.artist || 'LuvMusic';
  $('favorite').disabled = !song; $('favorite').textContent = song?.favorite ? '♥' : '♡';
  $('favorite').classList.toggle('liked', Boolean(song?.favorite));
}
async function selectAndPlay(song, autoplay = true) {
  if (!song) return;
  if (!ytReady) return notify('Trình phát YouTube đang tải, vui lòng thử lại.');
  try {
    await api(`/api/current/${song.id}`, {method:'POST'}); currentId = song.id; updatePlayerInfo(); render();
    autoplay ? ytPlayer.loadVideoById(song.youtube_id) : ytPlayer.cueVideoById(song.youtube_id);
  } catch (error) { notify(error.message); }
}
async function move(direction) {
  try {
    const data = await api(`/api/${direction}`, {method:'POST'}); songs = data.songs; currentId = data.current_id;
    await selectAndPlay(songs.find(song => song.id === currentId));
  } catch (error) { notify(error.message); }
}
async function toggleFavorite(id = currentId) {
  if (!id) return;
  try { await api(`/api/songs/${id}/favorite`, {method:'POST'}); await loadSongs(); }
  catch (error) { notify(error.message); }
}
async function removeSong(id) {
  try {
    const data = await api(`/api/songs/${id}`, {method:'DELETE'});
    if (id === currentId && ytReady) ytPlayer.stopVideo();
    currentId = data.current_id; notify(data.message); await loadSongs();
  } catch (error) { notify(error.message); }
}

$('songList').addEventListener('click', event => {
  const row = event.target.closest('.song'); if (!row) return;
  const song = songs.find(item => item.id === row.dataset.id), action = event.target.dataset.action;
  if (action === 'delete') removeSong(song.id); else if (action === 'favorite') toggleFavorite(song.id); else selectAndPlay(song);
});
$('play').addEventListener('click', () => {
  if (!ytReady) return notify('Trình phát YouTube đang tải.');
  if (!ytPlayer.getVideoData()?.video_id) { const song = getCurrent() || songs[0]; return song ? selectAndPlay(song) : $('modal').showModal(); }
  ytPlayer.getPlayerState() === YT.PlayerState.PLAYING ? ytPlayer.pauseVideo() : ytPlayer.playVideo();
});
$('playAll').addEventListener('click', () => songs[0] ? selectAndPlay(songs[0]) : $('modal').showModal());
$('previous').addEventListener('click', () => move('previous')); $('next').addEventListener('click', () => move('next'));
$('favorite').addEventListener('click', () => toggleFavorite());
$('volume').addEventListener('input', e => { if (ytReady) ytPlayer.setVolume(Number(e.target.value) * 100); });
$('progress').addEventListener('input', e => { if (ytReady) ytPlayer.seekTo(Number(e.target.value) / 100 * ytPlayer.getDuration(), true); });
$('search').addEventListener('input', () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadSongs, 220); });
async function shuffle() {
  try { const data = await api('/api/shuffle', {method:'POST'}); songs = data.songs; notify(data.message); render(); }
  catch (error) { notify(error.message); }
}
$('shuffle').addEventListener('click', shuffle); $('shuffleNav').addEventListener('click', shuffle);
$('repeat').addEventListener('click', () => {
  repeatMode = (repeatMode + 1) % 3; $('repeat').classList.toggle('selected', repeatMode > 0);
  $('repeat').textContent = repeatMode === 2 ? '↻¹' : '↻'; notify(['Đã tắt lặp lại', 'Lặp lại toàn bộ playlist', 'Lặp lại một bài'][repeatMode]);
});
document.querySelectorAll('.nav[data-view]').forEach(button => button.addEventListener('click', () => {
  view = button.dataset.view; document.querySelectorAll('.nav').forEach(item => item.classList.toggle('active', item === button)); loadSongs();
}));

const modal = $('modal');
$('openModal').addEventListener('click', () => modal.showModal()); $('close').addEventListener('click', () => modal.close()); $('cancel').addEventListener('click', () => modal.close());
$('addForm').addEventListener('submit', async event => {
  event.preventDefault(); $('error').textContent = '';
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    const data = await api('/api/songs', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    modal.close(); event.target.reset(); notify(data.message); await loadSongs(); await selectAndPlay(data.song);
  } catch (error) { $('error').textContent = error.message; }
});
loadSongs();
