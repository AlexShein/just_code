/**
 * @OnlyCurrentDoc
 */

// --- GLOBAL CONSTANTS ---
const SPREADSHEET = SpreadsheetApp.getActiveSpreadsheet()
const DASHBOARD_SHEET_NAME = "Dashboard"
const LOG_SHEET_NAME = "Data Log"
const SETTINGS_SHEET_NAME = "Settings"

// *** UPDATED: Cell locations for checkboxes and date picker ***
const DATE_PICKER_CELL = "B1"
const LOG_CHECKBOX_CELL = "C2"
const CLEAN_CHECKBOX_CELL = "D2"

// *** UPDATED: Data range on the dashboard ***
const DATA_RANGE_A1_NOTATION = "A4:D51"

const DASHBOARD_SHEET = SPREADSHEET.getSheetByName(DASHBOARD_SHEET_NAME)
const LOG_SHEET = SPREADSHEET.getSheetByName(LOG_SHEET_NAME)
const SETTINGS_SHEET = SPREADSHEET.getSheetByName(SETTINGS_SHEET_NAME)

// --- TRIGGERS & MENU ---

/**
 * Creates a custom menu in the spreadsheet UI when the file is opened.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Time Tracker")
    .addItem("Log Day's Activities", "logDailyActivities")
    .addItem("Clean Dashboard", "cleanDashboard")
    .addSeparator()
    .addItem("Load Data for Selected Date", "loadDataForDate") // New menu item
    .addToUi()
}

/**
 * Runs automatically when a user edits a cell.
 * @param {Object} e The event object from the edit.
 */
function onEdit(e) {
  const range = e.range
  const sheet = range.getSheet()

  if (sheet.getName() !== DASHBOARD_SHEET_NAME) return

  const a1Notation = range.getA1Notation()
  const isChecked = e.value === "TRUE"

  // --- Trigger for checkboxes ---
  if (isChecked) {
    if (a1Notation === LOG_CHECKBOX_CELL) {
      logDailyActivities()
      range.setValue(false)
    } else if (a1Notation === CLEAN_CHECKBOX_CELL) {
      cleanDashboard()
      range.setValue(false)
    }
  }

  // --- Trigger to fetch data when date is changed ---
  if (a1Notation === DATE_PICKER_CELL) {
    // *** UPDATED: Pass the event object 'e' to the function ***
    loadDataForDate(e)
  }
}

// --- CORE FUNCTIONS ---

/**
 * Fetches records from the Data Log for the selected date and displays them on the Dashboard.
 * Asks for confirmation if there is unsaved data on the dashboard.
 * @param {Object} e The event object from onEdit, used to revert changes if the user cancels.
 */
function loadDataForDate(e) {
  const ui = SpreadsheetApp.getUi()
  const dateToLoad = new Date(DASHBOARD_SHEET.getRange(DATE_PICKER_CELL).getValue())

  if (!dateToLoad || isNaN(dateToLoad.getTime())) {
    return // Exit silently if date is invalid
  }

  // --- NEW: Confirmation Logic ---
  const currentCategoryData = DASHBOARD_SHEET.getRange("B4:B51").getValues()
  const hasUnsavedData = currentCategoryData.some((row) => row[0] !== "")

  if (hasUnsavedData) {
    const response = ui.alert(
      "Overwrite Current Data?",
      "You have unsaved entries on the dashboard. Loading data from a past date will overwrite them. Are you sure you want to continue?",
      ui.ButtonSet.YES_NO,
    )

    if (response !== ui.Button.YES) {
      // If user cancels, revert the date picker to its previous value
      if (e && e.oldValue) {
        DASHBOARD_SHEET.getRange(DATE_PICKER_CELL).setValue(new Date(e.oldValue))
      }
      return // Stop the function
    }
  }
  // --- End of Confirmation Logic ---

  // Clear existing data on dashboard first
  const dashboardInputRange = DASHBOARD_SHEET.getRange("B4:D51")
  dashboardInputRange.clearContent()

  const logData = LOG_SHEET.getDataRange().getValues()
  const header = logData.shift() // Remove header

  const targetDate = dateToLoad.setHours(0, 0, 0, 0)
  const dataForDate = logData.filter((row) => {
    const rowDate = new Date(row[1]) // Date is in column 2 (index 1)
    return rowDate.setHours(0, 0, 0, 0) === targetDate
  })

  if (dataForDate.length === 0) {
    ui.toast(`No records found for ${new Date(targetDate).toLocaleDateString()}.`)
    return
  }

  const dataMap = new Map()
  const timezone = SPREADSHEET.getSpreadsheetTimeZone()
  dataForDate.forEach((row) => {
    const timeString = Utilities.formatDate(new Date(row[2]), timezone, "HH:mm")
    dataMap.set(timeString, [row[3], row[4], row[5]]) // Category, Satisfaction, Notes
  })

  const dashboardTimes = DASHBOARD_SHEET.getRange("A4:A51").getValues()
  const outputData = []

  dashboardTimes.forEach((timeRow) => {
    const time = timeRow[0]
    if (time instanceof Date) {
      const timeString = Utilities.formatDate(time, timezone, "HH:mm")
      if (dataMap.has(timeString)) {
        outputData.push(dataMap.get(timeString))
      } else {
        outputData.push(["", "", ""])
      }
    } else {
      outputData.push(["", "", ""])
    }
  })

  DASHBOARD_SHEET.getRange("B4:D51").setValues(outputData)
  ui.toast(`Loaded ${dataForDate.length} records for ${new Date(targetDate).toLocaleDateString()}.`)
}

/**
 * Clears the input columns on the Dashboard and sets default satisfaction.
 */
function cleanDashboard() {
  const ui = SpreadsheetApp.getUi()
  const response = ui.alert(
    "Clean Current Data?",
    "All data from the dashboard will be removed. Are you sure you want to continue?",
    ui.ButtonSet.YES_NO,
  )

  if (response !== ui.Button.YES) {
    return
  }

  DASHBOARD_SHEET.getRange("B4:B51").clearContent()
  DASHBOARD_SHEET.getRange("D4:D51").clearContent()

  const satisfactionRange = DASHBOARD_SHEET.getRange("C4:C51")
  const defaultSatisfactionValues = []
  for (let i = 0; i < 48; i++) {
    defaultSatisfactionValues.push([3])
  }
  satisfactionRange.setValues(defaultSatisfactionValues)

  SpreadsheetApp.getUi().alert("Dashboard has been cleaned.")
}

/**
 * Main function to log the activities from the Dashboard to the Data Log.
 */
function logDailyActivities() {
  const ui = SpreadsheetApp.getUi()
  const dateToLog = new Date(DASHBOARD_SHEET.getRange(DATE_PICKER_CELL).getValue())

  if (!dateToLog || isNaN(dateToLog.getTime())) {
    ui.alert("Error", "Please select a valid date in cell B1.", ui.ButtonSet.OK)
    return
  }

  const response = ui.alert(
    "Confirm Logging",
    `This will save the data for ${dateToLog.toLocaleDateString()}. Any existing data for this date will be overwritten. Continue?`,
    ui.ButtonSet.YES_NO,
  )

  if (response !== ui.Button.YES) {
    return
  }

  deleteRowsByDate(dateToLog)

  const dataRange = DASHBOARD_SHEET.getRange(DATA_RANGE_A1_NOTATION)
  const values = dataRange.getValues()

  const rowsToAdd = []
  for (let i = 0; i < values.length; i++) {
    const timeValue = values[i][0]
    if (!(timeValue instanceof Date) || !values[i][1]) {
      continue
    }

    const timestamp = new Date(dateToLog)
    timestamp.setHours(timeValue.getHours(), timeValue.getMinutes(), 0, 0)

    const category = values[i][1]
    const satisfaction = values[i][2]
    const notes = values[i][3]

    rowsToAdd.push([
      timestamp,
      new Date(dateToLog.setHours(0, 0, 0, 0)),
      timeValue,
      category,
      satisfaction,
      notes,
    ])
  }

  if (rowsToAdd.length > 0) {
    LOG_SHEET.getRange(LOG_SHEET.getLastRow() + 1, 1, rowsToAdd.length, rowsToAdd[0].length).setValues(
      rowsToAdd,
    )
    ui.alert(
      "Success",
      `Successfully logged ${rowsToAdd.length} entries for ${dateToLog.toLocaleDateString()}.`,
      ui.ButtonSet.OK,
    )
  } else {
    ui.alert("No Data", "No categories were selected on the Dashboard. Nothing was logged.", ui.ButtonSet.OK)
  }

  SpreadsheetApp.flush()
}

/**
 * Helper function to delete all rows from the Data Log for a specific date.
 */
function deleteRowsByDate(date) {
  const logData = LOG_SHEET.getDataRange().getValues()
  if (logData.length < 2) return

  const targetDate = new Date(date.setHours(0, 0, 0, 0)).getTime()
  const rowsToDelete = []

  for (let i = 1; i < logData.length; i++) {
    const rowDate = new Date(logData[i][1])
    if (rowDate.getTime() === targetDate) {
      rowsToDelete.push(i + 1)
    }
  }

  for (let i = rowsToDelete.length - 1; i >= 0; i--) {
    LOG_SHEET.deleteRow(rowsToDelete[i])
  }
}
