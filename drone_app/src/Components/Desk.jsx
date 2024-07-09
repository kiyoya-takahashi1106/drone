import React, { useState, useEffect } from 'react';

const Desk = ({ N, M }) => {
    const [deskSizes, setDeskSizes] = useState([]);

    useEffect(() => {
        const calculateSizes = () => {
            const sizes = [];
            for (let i = 0; i < N * M; i++) {
                let deskHeight, deskWidth;
                const heightFlag = (60 * N + 40 * (N - 1) <= 360);
                const widthFlag = (100 * M + 60 * (M - 1) <= 740);

                if (heightFlag && widthFlag) {
                    deskHeight = 60;
                    deskWidth = 100;
                } else if (heightFlag) {   // widthを基に求めたい
                    const _ = 740 / (M + (3 / 5) * (M - 1));
                    deskWidth = _;
                    deskHeight = _ * (3 / 5);
                } else if (widthFlag) {   // heightを基に求めたい
                    const _ = 360 / (N + (2 / 3) * (N - 1));
                    deskHeight = _;
                    deskWidth = _ * (5 / 3);
                } else {
                    const _width = 740 / (M + (3 / 5) * (M - 1));
                    const _height = 360 / (N + (2 / 3) * (N - 1));
                    const __width = _height * (5 / 3);
                    const __height = _width * (3 / 5);
                    if ((__height * N + __height * (2 / 3) * (N - 1) <= 360)) {
                        deskHeight = __height;
                        deskWidth = _width;
                    } else {
                        deskHeight = _height;
                        deskWidth = __width;
                    }
                }
                sizes.push({ height: deskHeight, width: deskWidth });
            }
            setDeskSizes(sizes);
        };

        calculateSizes();
    }, [N, M]);

    return (
        <div style={{ display: 'grid', gridTemplateColumns: `repeat(${M}, auto)`, gap: `${deskSizes.length > 0 ? deskSizes[0].height * (2 / 3) : 0}px ${deskSizes.length > 0 ? deskSizes[0].height : 0}px` }}>
            {deskSizes.map((size, index) => (
                <div
                    key={index}
                    style={{
                        height: `${size.height}px`,
                        width: `${size.width}px`,
                        backgroundColor: 'white',
                        border: '1px solid black'
                    }}
                ></div>
            ))}
        </div>
    );
};

export default Desk;
