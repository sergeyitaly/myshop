import { Slider } from '@mui/material';
import { ChangeEvent, useEffect, useState } from 'react';
import styles from './RangeSlider.module.scss'
import { formatPrice } from '../../../functions/formatPrice';
import { formatNumber } from '../../../functions/formatNumber';
import { useDebounce } from '../../../hooks/useDebounce';


interface AppRangeSliderPeops {
    value: [number, number]
    minValue: number
    maxValue: number
    changePrice: (priceRange: [number, number]) => void
}

export const AppRangeSlider = ({
    value,
    minValue,
    maxValue,
    changePrice
}: AppRangeSliderPeops) => {

    const minDistance = 1000;

    const [startValue1FromScratch, setStartValue1FromScratch] = useState<boolean>(true) 

    const value1 = useDebounce(value[0].toString(), 1000)
    const value2 = useDebounce(value[1].toString(), 1000)

    console.log('min-max', minValue, maxValue);
    console.log(value1, value2);
    
    
    
    useEffect(() => {
        
            if(+value1 < minValue){
                changePrice([minValue, value[1]])
            }
    
            if(+value1 > value[1]){
                changePrice([value[1], value[1]])
            }

        setStartValue1FromScratch(true)
    }, [value1, minValue])
   
    useEffect(() => {

        if(+value2 < value[0]){
            changePrice([value[0], value[0]])
        }
        
    }, [value2, maxValue])

    useEffect(() => {
        if(+value2 === 0){
            changePrice([minValue, maxValue])
        }
    }, [])


    const handleChange2 = (
      _: Event,
      newValue: number | number[],
      activeThumb: number,
    ) => {
        
      if (!Array.isArray(newValue)) {
        return;
      }
  
      if (newValue[1] - newValue[0] < minDistance) {
        if (activeThumb === 0) {
          const clamped = Math.min(newValue[0],maxValue - minDistance);
          changePrice([clamped, clamped + minDistance]);
        } else {
          const clamped = Math.max(newValue[1], minDistance);
          changePrice([clamped - minDistance, clamped]);
        }
      } else {
        changePrice(newValue as [number, number]);
      }
    };

    const handleChangeInp1 = (e: ChangeEvent<HTMLInputElement>) => {

        
        let transformedValue = parseFloat(e.target.value.replace(/\s/g, '').replace(/,/g, '.'))

        if(startValue1FromScratch){
            
            const lastIndex = transformedValue.toString().length
            
            transformedValue = +transformedValue.toString()[lastIndex - 1]
        }
        
        if(!e.target.value){
            transformedValue = 0
        }
        
       

        if(!isNaN(+transformedValue) && transformedValue <= maxValue){
            changePrice([transformedValue, value[1]])
        }

        setStartValue1FromScratch(false)



    }

    const handleChangeInp2 = (e: ChangeEvent<HTMLInputElement>) => {
        let transformedValue = parseFloat(e.target.value.replace(/\s/g, '').replace(/,/g, '.'))
        if(!e.target.value){
            transformedValue = 0
        }
        if(!isNaN(+transformedValue) && transformedValue <= maxValue){
            changePrice([value[0], transformedValue])
        }
    }

    return (
        <div className={styles.appSlider}>
            <Slider
                getAriaLabel={() => 'Minimum distance shift'}
                value={value}
                onChange={handleChange2}
                disableSwap
                min = {minValue}
                max = {maxValue}
                classes={{
                    thumb: styles.thumb,
                    active: styles.active,
                    rail: styles.rail,
                    track: styles.track
                }}
            />
            <div className={styles.priceRange}>
                <span>{formatPrice(value[0], 'UAH') }</span>
                <span>{formatPrice(value[1], 'UAH')}</span>
            </div>
            <div className={styles.inputContainer}>
                <input 
                    type="text" 
                    value={formatNumber(value[0], 0) }
                    onChange={handleChangeInp1}
                />
                <input 
                    type="text" 
                    value={formatNumber(value[1], 0)}
                    onChange={handleChangeInp2}
                />
            </div>
        </div>
    )
}