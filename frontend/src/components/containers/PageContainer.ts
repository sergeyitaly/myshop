import styled from '@emotion/styled'
import { screen } from '../../constants'

export const PageContainer = styled.div`
    padding-left: clamp(0.75rem, 2.087vw + 0.098rem, 2.063rem);
    padding-right: clamp(0.75rem, 2.087vw + 0.098rem, 2.063rem);
    margin: 0 auto;
    max-width: ${screen.maxBig};
`