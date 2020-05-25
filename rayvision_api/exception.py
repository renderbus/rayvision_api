"""CG errors."""

from future.moves.urllib.request import HTTPErrorProcessor


class RayvisionError(Exception):
    """Raise RayvisionError if something wrong."""

    def __init__(self, error_code, error, *args, **kwargs):
        """Initialize error message, inherited Exception.

        Args:
            error_code (int): Error status code.
            error (str): Error message.
            args (set): Other parameters.
            kwargs (dict): Other keyword parameters.

        """
        super(RayvisionError, self).__init__(self, error, *args, **kwargs)
        self.error_code = error_code
        self.error = error

    def __str__(self):
        """Let its  object  out an error message."""
        return 'RayvisionError: {0}: {1}'.format(self.error_code, self.error)


class RayvisonTaskIdError(RayvisionError):
    """Raise RayVisonTaskIdError."""

    def __init__(self, error_code, error):
        """Initialize Task error message, inherited RayvisionError."""
        super(RayvisionError, self).__init__(error_code, error)
        self.error_code = 2000
        self.error = error

    def __str__(self):
        """Let its  object  out an error message."""
        return 'Error code: {}, Error message: {}'.format(
            self.error_code,
            self.error,
        )


class RayvisionAPIError(RayvisionError):
    """Raise RayVisionAPIError."""

    def __init__(self, error_code, error, request):
        """Initialize API error message, inherited RayvisionError.

        Args:
            error_code (int): Error status code.
            error (object): Error message.
            request (str): Request url.

        """
        super(RayvisionAPIError, self).__init__(error_code, error)
        self.error_code = error_code
        self.error = error
        self.request = request

    def __str__(self):
        """Let its  object print out an error message."""
        return 'Error code: {}, Error message: {}, URL: {}'.format(
            self.error_code,
            self.error,
            self.request)


# pylint: disable=no-init
class RayvisionHTTPErrorProcessor(HTTPErrorProcessor):
    """Process HTTP error responses.

    Inherit HTTPErrorProcessor in urllib2.

    """

    def http_response(self, request, response):
        """Override the http_response method of HTTPErrorProcessor.

        Process the response,when it is a bad Request,the corresponding
        exception is reported.

        Args:
            request (urllib2.Request): Request object.
            response (opener.open): Response object.

        Returns:
            Exception: Abnormal response.

        """
        code, msg, data = response.code, response.msg, response.info()

        # According to RFC 2616, "2xx" code indicates that the client's
        # request was successfully received, understood, and accepted.
        if (not 200 <= code < 300) and code != 400:
            response = self.parent.error(
                'http', request, response, code, msg, data)

        return response


class AnalyzeError(Exception):
    """Analyze has a damage error."""


class MaxDamageError(AnalyzeError):
    """Max has a damage error."""


class MaxExeNotExistError(AnalyzeError):
    """There are no errors in the Max startup file."""


class CGExeNotExistError(AnalyzeError):
    """No errors in CG boot."""


class ProjectMaxVersionError(AnalyzeError):
    """Project Max version error."""


class GetCGVersionError(AnalyzeError):
    """Error getting CG version."""


class GetRendererError(AnalyzeError):
    """Get renderer error."""


class GetCGLocationError(AnalyzeError):
    """Error getting CG local path."""


class MultiScatterAndVrayConfilictError(AnalyzeError):
    """Multi scatter and vray Confilict error."""


class VersionNotMatchError(AnalyzeError):
    """Version not match error."""


class CGFileNotExistsError(AnalyzeError):
    """CG file does not exist error."""


class CGFileZipFailError(AnalyzeError):
    """CG file compression failed error."""


class CGFileNameIllegalError(AnalyzeError):
    """CG File Name Illegal Error."""


class AnalyseFailError(AnalyzeError):
    """Analyse Fail Error."""


class FileNameContainsChineseError(AnalyzeError):
    """File Name Contains Chinese Error."""


class CompressionFailedError(Exception):
    """Compression failed error."""


class DecompressionFailedError(Exception):
    """Unzip failed error."""


class UploadFileNotSupportError(Exception):
    """Upload_file_name_only support does_not_support error."""