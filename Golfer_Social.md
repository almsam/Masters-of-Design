# MDes group scheduler

### Step 1, insert the code:

Create a google Sheet - go to **Extensions** -> **Apps Script**

delete the code in place and paste in the big code block on bottom - then click save on the top

### Step 2, set up the sheet:

rename the sheet (bottom of the sheets UI) and name it `Setup`

In `B1` write the number of people per group
In `B2` write the number of time slots
in `A1:A11` write the names of all the people

### Step 3, run the script:

Save n refresh the page - press **Meeting Scheduler** -> **Generate Schedule**

Approve all permisions and neew sheets will pop up

```
/**
 * MEETING SCHEDULER — maximizes unique pairings across time slots,
 * splits people into tables, and rotates the leader role fairly.
 *
 * https://en.wikipedia.org/wiki/Social_golfer_problem
 *
 * Sheet labeled 'Setup':
 * B1 = table size (like 4)
 * B2 = number of time slots (like 6)
 * A5:A... = list of names (one per row, starting row 5)
 */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Meeting Scheduler')
    .addItem('Generate Schedule', 'generateSchedule')
    .addToUi();
}

function generateSchedule() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const setup = ss.getSheetByName('Setup');
  if (!setup) throw new Error('Create a "Setup" sheet first (see instructions).');

  const groupSize = setup.getRange('B1').getValue();
  const numSlots = setup.getRange('B2').getValue();
  const lastRow = setup.getLastRow();
  const names = setup.getRange('A5:A' + lastRow).getValues().flat().filter(String);
  const n = names.length;

  if (!groupSize || !numSlots || n < groupSize) {
    throw new Error('Check Setup sheet: table size (B1), number of slots (B2), names from A5 down.');
  }

  const numGroups = Math.ceil(n / groupSize);

  // met[i][j] = how many times person i and j have shared a meet
  const met = Array.from({ length: n }, () => new Array(n).fill(0));
  // leadCount[i] = how many times person i has been leader
  const leadCount = new Array(n).fill(0);

  const scheduleOutput = [];

  for (let s = 0; s < numSlots; s++) {
    const groups = buildBestGrouping(n, numGroups, met);

    // update "met" counts for this slot's groups
    groups.forEach(g => {
      for (let a = 0; a < g.length; a++) {
        for (let b = a + 1; b < g.length; b++) {
          met[g[a]][g[b]]++;
          met[g[b]][g[a]]++;
        }
      }
    });

    // pick leader per group first - whoever in that group has led the fewest times so far
    const leaders = groups.map(g => {
      const minCount = Math.min(...g.map(i => leadCount[i]));
      const candidates = g.filter(i => leadCount[i] === minCount);
      const leader = candidates[Math.floor(Math.random() * candidates.length)];
      leadCount[leader]++;
      return leader;
    });

    scheduleOutput.push({ slot: s + 1, groups, leaders });
  }

  writeScheduleToSheet(ss, names, scheduleOutput);
  writeMatrixToSheet(ss, names, met);

  SpreadsheetApp.getUi().alert('Schedule generated! See the "Schedule" and "Meeting Matrix" tabs.');
}

function buildBestGrouping(n, numGroups, met) {
  const indices = [...Array(n).keys()];
  let best = null;
  let bestScore = Infinity;

  // first we shal try many random groupings, keep the one with fewest repete pairings
  const TRIALS = 150;
  for (let t = 0; t < TRIALS; t++) {
    const shuffled = shuffleArray(indices.slice());
    const groups = chunkIntoGroups(shuffled, numGroups);
    const score = scoreGrouping(groups, met);
    if (score < bestScore) {
      bestScore = score;
      best = groups;
    }
  }

  // this will be hill-climb by swapping two people between tables if it helps
  const SWAP_TRIALS = 400;
  for (let t = 0; t < SWAP_TRIALS; t++) {
    const g1 = Math.floor(Math.random() * best.length);
    const g2 = Math.floor(Math.random() * best.length);
    if (g1 === g2 || best[g1].length === 0 || best[g2].length === 0) continue;
    const i1 = Math.floor(Math.random() * best[g1].length);
    const i2 = Math.floor(Math.random() * best[g2].length);

    const trial = best.map(g => g.slice());
    const tmp = trial[g1][i1];
    trial[g1][i1] = trial[g2][i2];
    trial[g2][i2] = tmp;

    const newScore = scoreGrouping(trial, met);
    if (newScore < bestScore) {
      best = trial;
      bestScore = newScore;
    }
  }

  return best;
}

function scoreGrouping(groups, met) {
  let score = 0;
  groups.forEach(g => {
    for (let a = 0; a < g.length; a++) {
      for (let b = a + 1; b < g.length; b++) {
        score += met[g[a]][g[b]];
      }
    }
  });
  return score;
}

function chunkIntoGroups(indices, numGroups) {
  const groups = Array.from({ length: numGroups }, () => []);
  indices.forEach((idx, i) => groups[i % numGroups].push(idx));
  return groups;
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function writeScheduleToSheet(ss, names, scheduleOutput) {
  let sheet = ss.getSheetByName('Schedule');
  if (sheet) ss.deleteSheet(sheet);
  sheet = ss.insertSheet('Schedule');

  let row = 1;
  scheduleOutput.forEach(({ slot, groups, leaders }) => {
    sheet.getRange(row, 1).setValue(`Time Slot ${slot}`).setFontWeight('bold');
    row++;
    groups.forEach((g, gi) => {
      const memberNames = g.map(i => names[i]);
      const leaderName = names[leaders[gi]];
      sheet.getRange(row, 1).setValue(`Table ${gi + 1}`);
      sheet.getRange(row, 2).setValue(memberNames.join(', '));
      sheet.getRange(row, 3).setValue(`Leader: ${leaderName}`);
      row++;
    });
    row++; // blank line between co horts
  });
  sheet.autoResizeColumns(1, 3);
}

function writeMatrixToSheet(ss, names, met) {
  let sheet = ss.getSheetByName('Meeting Matrix');
  if (sheet) ss.deleteSheet(sheet);
  sheet = ss.insertSheet('Meeting Matrix');

  sheet.getRange(1, 2, 1, names.length).setValues([names]);
  sheet.getRange(2, 1, names.length, 1).setValues(names.map(nm => [nm]));
  sheet.getRange(2, 2, names.length, names.length).setValues(met);
  sheet.autoResizeColumns(1, names.length + 1);
}
```