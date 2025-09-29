
console.debug('[app] static JS loaded');


const ideas = [
  'Ship something small today',
  'Record a build log clip',
  'Refactor one messy function',
  'Write a README improvement',
  'Invite a friend to join'
];

function injectIdea() {
  const host = document.querySelector('.idea-generator');
  if (!host) return;
  let idx = 0;
  host.textContent = ideas[idx];
  setInterval(() => {
    idx = (idx + 1) % ideas.length;
    host.textContent = ideas[idx];
  }, 4000);
}

window.addEventListener('DOMContentLoaded', injectIdea);