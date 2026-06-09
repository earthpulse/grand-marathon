<script>
    let { dates = [], selected = $bindable(""), today = "", date_colors = {} } = $props();

    // Parse year and month from the available dates (default to August 2025)
    const currentMonthData = $derived.by(() => {
        if (!Array.isArray(dates) || dates.length === 0) {
            return { year: 2025, month: 7 }; // August is index 7
        }
        // Look for the first date with a valid format
        const firstDateStr =
            dates.find((d) => typeof d === "string" && d.includes("-")) ||
            "2025-08-01";
        const parts = firstDateStr.split("-");
        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1; // 0-indexed
        return { year, month };
    });

    const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    const weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

    // Compute the calendar grid cells for the current month
    const calendarCells = $derived.by(() => {
        const { year, month } = currentMonthData;

        // Days in the month
        const totalDays = new Date(year, month + 1, 0).getDate();

        // First day of the week index (0 = Sunday, 1 = Monday, etc.)
        const firstDayOfWeek = new Date(year, month, 1).getDay();

        const cells = [];

        // Prepend empty cells for alignment
        for (let i = 0; i < firstDayOfWeek; i++) {
            cells.push({ day: null, dateStr: null });
        }

        // Populate actual days of the month
        for (let day = 1; day <= totalDays; day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
            cells.push({ day, dateStr });
        }

        return cells;
    });

    let showGrid = $state(false);

    $effect(() => {
        if (selected && selected !== "2025-08-15" && selected !== "2025-08-22") {
            showGrid = true;
        }
    });

    function selectDate(dateStr) {
        if (dateStr && dates.includes(dateStr)) {
            selected = dateStr;
        }
    }
</script>

<div
    class="bg-white border border-gray-200 rounded-xl p-2 shadow-xs hover:shadow-sm transition-all duration-200 flex flex-col gap-1.5 w-full"
>
    <!-- Calendar Month Header -->
    <div class="flex items-center justify-between px-0.5">
        <h3 class="text-[11px] font-bold text-gray-900 flex items-center gap-1">
            📅 {monthNames[currentMonthData.month]}
            {currentMonthData.year}
        </h3>
        <span
            class="text-[8px] font-bold text-gray-400 bg-gray-50 px-1 py-0.5 rounded-full border border-gray-100"
        >
            Timeline
        </span>
    </div>

    <!-- Quick Select Buttons -->
    <div class="grid grid-cols-3 gap-1.5">
        <button
            onclick={() => {
                selectDate("2025-08-15");
                showGrid = false;
            }}
            class="py-1 px-1 border rounded-md text-[9px] font-bold transition-all duration-150 cursor-pointer flex items-center justify-center gap-0.5
                {selected === '2025-08-15' && !showGrid
                ? 'bg-gray-900 text-white border-gray-900 shadow-xs'
                : 'bg-white hover:bg-gray-50 border-gray-200 text-gray-700'}"
        >
            📅 TODAY
        </button>
        <button
            onclick={() => {
                selectDate("2025-08-22");
                showGrid = false;
            }}
            class="py-1 px-1 border rounded-md text-[9px] font-bold transition-all duration-150 cursor-pointer flex items-center justify-center gap-0.5
                {selected === '2025-08-22' && !showGrid
                ? 'bg-gray-900 text-white border-gray-900 shadow-xs'
                : 'bg-white hover:bg-gray-50 border-gray-200 text-gray-700'}"
        >
            🗓️ 7 DAYS
        </button>
        <button
            onclick={() => {
                showGrid = true;
            }}
            class="py-1 px-1 border rounded-md text-[9px] font-bold transition-all duration-150 cursor-pointer flex items-center justify-center gap-0.5
                {showGrid
                ? 'bg-gray-900 text-white border-gray-900 shadow-xs'
                : 'bg-white hover:bg-gray-50 border-gray-200 text-gray-700'}"
        >
            📅 PICK DATE
        </button>
    </div>

    <!-- Calendar Grid -->
    {#if showGrid}
        <div class="flex flex-col gap-0.5 mt-1">
            <!-- Weekdays Row -->
            <div class="grid grid-cols-7 gap-0.5 text-center">
                {#each weekdays as day}
                    <span
                        class="text-[8px] font-bold text-gray-400 uppercase tracking-wider h-4 flex items-center justify-center"
                    >
                        {day}
                    </span>
                {/each}
            </div>

            <!-- Days Grid -->
            <div class="grid grid-cols-7 gap-0.5 justify-items-stretch">
                {#each calendarCells as cell}
                    {#if cell.day === null}
                        <div class="aspect-square w-full"></div>
                    {:else}
                        {@const isAvailable = dates.includes(cell.dateStr)}
                        {@const isSelected = selected === cell.dateStr}
                        {@const isToday =
                            cell.dateStr &&
                            today &&
                            (cell.dateStr === today ||
                                cell.dateStr.slice(5) === today.slice(5))}
                        {@const isFuture =
                            cell.dateStr &&
                            today &&
                            cell.dateStr.slice(5) > today.slice(5)}
                        {@const dayColor = date_colors[cell.dateStr] || "green"}

                        <button
                            onclick={() => selectDate(cell.dateStr)}
                            disabled={!isAvailable}
                            title={isAvailable
                                ? `${cell.dateStr}${isToday ? " (Today)" : isFuture ? " (Forecasted)" : ""}`
                                : "No data"}
                            class="aspect-square w-full rounded-md text-[9px] font-bold flex items-center justify-center transition-all relative focus:outline-hidden
                                {isAvailable
                                ? 'cursor-pointer font-bold'
                                : 'cursor-not-allowed opacity-30 font-normal'}
                                {isSelected
                                ? 'bg-gray-900 text-white'
                                : isAvailable
                                  ? dayColor === 'red'
                                    ? 'bg-red-50/70 text-red-800 hover:bg-red-100/90'
                                    : dayColor === 'yellow'
                                      ? 'bg-amber-50/70 text-amber-800 hover:bg-amber-100/90'
                                      : 'bg-emerald-50/70 text-emerald-800 hover:bg-emerald-100/90'
                                  : 'text-gray-300'}
                                {isToday
                                ? 'border-2 border-gray-900'
                                : isFuture
                                  ? 'border border-dashed border-gray-300'
                                  : 'border border-transparent'}"
                        >
                            {cell.day}
                        </button>
                    {/if}
                {/each}
            </div>
        </div>
    {/if}
</div>
