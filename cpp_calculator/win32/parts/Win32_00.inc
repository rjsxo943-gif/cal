#define UNICODE
#define _UNICODE

#include <windows.h>
#include <commctrl.h>
#include <windowsx.h>

#include <algorithm>
#include <array>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "ScientificCalculator.h"

#pragma comment(lib, "Comctl32.lib")
#pragma comment(linker, "\"/manifestdependency:type='win32' name='Microsoft.Windows.Common-Controls' version='6.0.0.0' processorArchitecture='*' publicKeyToken='6595b64144ccf1df' language='*'\"")

namespace {

using calculator::core::CalculatorController;
using calculator::core::CalculatorError;
using calculator::core::InvalidInputError;
using calculator::modes::ComplexController;
using calculator::modes::EquationController;
using calculator::modes::StatisticsController;

constexpr wchar_t kWindowClass[] = L"ScientificCalculatorWin32Class";
constexpr wchar_t kWindowTitle[] = L"Scientific Calculator - C++ Win32";

enum class AppMode { Calc, Statistics, Equation, Complex };

enum ControlId : int {
    IdTitle = 100,
    IdStatus,
    IdModeCalc,
    IdModeStat,
    IdModeEqn,
    IdModeComplex,
    IdHistory,
    IdHistoryClear,

    IdExpression = 200,
    IdResult,
    IdShift,
    IdDrg,
    IdFormat,
    IdFraction,
    IdCursorLeft,
    IdDelete,
    IdSin,
    IdCos,
    IdTan,
    IdLog,
    IdLn,
    IdSqrt,
    IdNpr,
    IdNcr,
    IdGcd,
    IdLcm,
    IdMod,
    IdAbs,
    Id7,
    Id8,
    Id9,
    IdLeftParen,
    IdRightParen,
    IdDivide,
    Id4,
    Id5,
    Id6,
    IdMultiply,
    IdPercent,
    IdFactorial,
    Id1,
    Id2,
    Id3,
    IdMinus,
    IdPi,
    IdE,
    Id0,
    IdDecimal,
    IdAns,
    IdPlus,
    IdClear,
    IdEquals,
    IdReciprocal,
    IdQuot,
    IdRem,
    IdRandom,
    IdRandInt,
    IdCursorRight,

    IdStatInstruction = 400,
    IdStatInput,
    IdStatAdd,
    IdStatRemove,
    IdStatClear,
    IdStatList,
    IdStatSummary,

    IdEqnInstruction = 500,
    IdEqnLabelA,
    IdEqnA,
    IdEqnLabelB,
    IdEqnB,
    IdEqnLabelC,
    IdEqnC,
    IdEqnSolve,
    IdEqnResult,

    IdComplexInstruction = 600,
    IdComplexRect,
    IdComplexPolar,
    IdComplexLabelFirst,
    IdComplexFirst,
