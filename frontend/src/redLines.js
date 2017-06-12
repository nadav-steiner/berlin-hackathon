export function getRedLine(dataSeries) {
    return {
        name: 'Values',
        data: dataSeries,
        color: 'red',
        lineWidth: 1,
        marker: {
            radius: 4,
        },
        enableMouseTracking: false,
    };
}